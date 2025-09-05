<?php

namespace App\Http\Controllers;
use App\Models\User;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Hash;

class UserController extends Controller
{
    public function create_user(Request $request)
    {
        $user = new User;
        $user-> name = $request->name;
        $user-> email = $request->email;
        $user-> password = bcrypt($request->password);
        $user->save();
        return response()->json($user, 201);
    }

    public function login(Request $request)
    {
        $user = User::where('email', $request->email)->first();
        if (! $user || !hash::check($request->password, $user->password)){
            return response()->json(['message'=> 'credenciales invalidas'], 401);
        }
        $token = $user->createToken('auth_token')->plainTextToken;
        return response()->json([
            'access_token' => $token,
            'user_name'=>$user->name
        ]);
    }
}