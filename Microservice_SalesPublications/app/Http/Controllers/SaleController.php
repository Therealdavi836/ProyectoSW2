<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Sale;
use App\Models\Publication;
use Illuminate\Support\Facades\Http;

class SaleController extends Controller
{
    private $authServiceUrl;
    private $gatewayUrl;

    public function __construct()
    {
        $this->authServiceUrl = env('AUTH_URL', 'http://auth-ms:8000/api/me');
        $this->gatewayUrl   = env('GATEWAY_URL', 'http://auth-ms:8000/api/forward');
    }

    // ================================
    // Helper para validar usuario en Auth MS
    // ================================
    private function getAuthenticatedUser(Request $request)
    {
        $token = $request->bearerToken();
        if ($token && !str_starts_with($token, 'Bearer ')) {
            $token = 'Bearer ' . $token;
        }

        $response = Http::withToken($token)->get($this->authServiceUrl);

        if ($response->failed()) return null;

        $user = $response->json();
        return [
            'id'    => $user['id'],
            'name'  => $user['name'],
            'email' => $user['email'],
            'role'  => $user['role'], // lo que devuelve Auth MS
        ];
    }
    
    // ================================
    // Listar ventas (según rol)
    // ================================
    public function index(Request $request)
    {
        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);

        if ($user['role'] === 'admin') {
            return Sale::with('publication')->get();
        }

        if ($user['role'] === 'customer') {
            return Sale::with('publication')->where('customer_id', $user['id'])->get();
        }

        if ($user['role'] === 'seller') {
            return Sale::with('publication')->where('seller_id', $user['id'])->get();
        }

        return response()->json(['error' => 'No autorizado'], 403);
    }

    // ================================
    // Registrar una venta (solo customer)
    // ================================
    public function store(Request $request)
    {
        $validated = $request->validate([
            'publication_id' => 'required|exists:publications,id',
            'sale_price'     => 'required|numeric|min:0'
        ]);

        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);

        if ($user['role'] !== 'customer') {
            return response()->json(['error' => 'Solo clientes pueden comprar'], 403);
        }

        $publication = Publication::findOrFail($validated['publication_id']);

        if ($publication->status !== 'activo') {
            return response()->json(['error' => 'La publicación no está disponible'], 400);
        }

        $sale = Sale::create([
            'publication_id' => $publication->id,
            'customer_id'    => $user['id'],
            'seller_id'      => $publication->user_id,
            'sale_price'     => $validated['sale_price'],
            'sale_date'      => now()
        ]);

        $publication->status = 'vendido';
        $publication->save();

        // Notificaciones vía gateway
        $notifications = [
            [
                'user_id' => $sale->seller_id,
                'title'   => 'Venta confirmada',
                'message' => 'Has vendido tu vehículo exitosamente.',
                'type'    => 'success'
            ],
            [
                'user_id' => $sale->customer_id,
                'title'   => 'Compra exitosa',
                'message' => 'Has comprado un vehículo. Revisa tus detalles de compra en tu cuenta.',
                'type'    => 'info'
            ]
        ];

        foreach ($notifications as $note) {
            Http::withToken($request->bearerToken())
                ->post("{$this->gatewayUrl}/notifications", $note);
        }

        return response()->json($sale, 201);
    }

    // ================================
    // Ver detalle de una venta
    // ================================
    public function show(Request $request, $id)
    {
        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);

        $sale = Sale::with('publication')->findOrFail($id);

        if ($user['role'] === 'customer' && $sale->customer_id !== $user['id']) {
            return response()->json(['error' => 'No autorizado'], 403);
        }

        if ($user['role'] === 'seller' && $sale->seller_id !== $user['id']) {
            return response()->json(['error' => 'No autorizado'], 403);
        }

        return $sale;
    }
}
