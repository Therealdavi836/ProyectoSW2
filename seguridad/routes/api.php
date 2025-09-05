<?php

use App\Http\Controllers\UserController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

//Ruta para crear usuarios por metodo API sanctum 
Route::post('/create_user',[UserController::class, 'create_user']);

//Ruta para iniciar sesión en la base de datos
Route::post('/login', [UserController::class, 'login']);