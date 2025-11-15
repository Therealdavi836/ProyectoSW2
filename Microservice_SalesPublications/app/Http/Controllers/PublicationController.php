<?php

namespace App\Http\Controllers;

use Illuminate\Http\Request;
use App\Models\Publication;
use Illuminate\Support\Facades\Http;

class PublicationController extends Controller
{
    private $authServiceUrl;
    private $gatewayUrl;

    public function __construct()
    {
        $this->authServiceUrl = 'http://localhost:8000/api/me'; // Auth MS
        $this->gatewayUrl = 'http://localhost:8000/api/forward'; // Gateway
    }

    // Validar token directamente con Auth MS (evita loop)
    private function getAuthenticatedUser(Request $request)
    {
        $token = $request->bearerToken();
        if (!$token) return null;

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

    public function index(Request $request)
    {
        return Publication::where('status', 'activo')
            ->when($request->has('user_id'), fn($q) => $q->where('user_id', $request->query('user_id')))
            ->get();
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'vehicle_id'  => 'required|string',
            'title'       => 'required|string',
            'description' => 'nullable|string',
            'price'       => 'required|numeric|min:0'
        ]);

        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);
        if ($user['role'] !== 'seller') return response()->json(['error' => 'Solo vendedores pueden publicar'], 403);

        // Validar vehículo por gateway -> catalog
        $catalogResponse = Http::withToken($request->bearerToken())
            ->get("{$this->gatewayUrl}/catalog/{$validated['vehicle_id']}");

        if ($catalogResponse->failed()) {
            return response()->json(['error' => 'El vehículo no existe en el catálogo'], 400);
        }

        $publication = Publication::create([
            'user_id'    => $user['id'],
            'vehicle_id' => $validated['vehicle_id'],
            'title'      => $validated['title'],
            'description'=> $validated['description'] ?? null,
            'price'      => $validated['price'],
            'status'     => 'activo'
        ]);

        // Notificación por gateway -> notifications
        Http::withToken($request->bearerToken())
            ->post("{$this->gatewayUrl}/notifications", [
                'user_id' => $publication->user_id,
                'title'   => 'Publicación creada',
                'message' => 'Tu vehículo fue publicado exitosamente.',
                'type'    => 'success'
            ]);

        return response()->json($publication, 201);
    }

    public function show($id) { return Publication::findOrFail($id); }

    public function update(Request $request, $id)
    {
        $publication = Publication::findOrFail($id);
        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);
        if ($user['role'] !== 'seller' || $publication->user_id !== $user['id']) {
            return response()->json(['error' => 'No autorizado'], 403);
        }

        $publication->update($request->only(['title','description','price']));
        return response()->json($publication);
    }

    public function destroy(Request $request, $id)
    {
        $publication = Publication::findOrFail($id);
        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);
        if ($user['role'] !== 'seller' || $publication->user_id !== $user['id']) {
            return response()->json(['error' => 'No autorizado'], 403);
        }

        $publication->delete();
        return response()->json(['message' => 'Publicación eliminada']);
    }

    public function changeStatus(Request $request, $id)
    {
        $publication = Publication::findOrFail($id);
        $user = $this->getAuthenticatedUser($request);
        if (!$user) return response()->json(['error' => 'Usuario no autenticado'], 401);
        if ($user['role'] !== 'seller' || $publication->user_id !== $user['id']) {
            return response()->json(['error' => 'No autorizado'], 403);
        }

        $request->validate(['status' => 'required|in:activo,inactivo,vendido']);
        $publication->status = $request->status;
        $publication->save();

        return response()->json($publication);
    }
}
