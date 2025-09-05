# API en Flask de python para divisas
#Importamos flask, metodo jsonify para convertir a json, request para traer datos del json y math para sqrt
from flask import Flask, jsonify, request #Imports de los elementos de Flask
from pymongo import MongoClient #Importamos la conexion con la db

#definimos el app por el cual Flask funcionara
app = Flask(__name__)
client = MongoClient("mongodb://localhost:27017/") #Conexion con la base de datos
db = client["Divisas"]#traemos la base de datos de divisas
divisas_collection = db["Valor_Divisas"]#Definimos especificamente el documento donde iran los registros

#Metodo divisas para agregarlas en la base de datos, usando POST
@app.route('/divisas', methods=['POST'])
def agregar_divisas():
    data = request.get_json() #Traemos el json que nos envian
    result = divisas_collection.insert_one({ #Insertamos el json en la base de datos
        "origen":data["origen"],
        "destino":data["destino"],
        "valor":float(data["valor"])
    })
    return jsonify({ #Retornamos un mensaje de exito
        "mensaje": "Divisa guardada correctamente",
        "id": str(result.inserted_id)
    }), 201

#Tasas de cambio como ejemplificacion para convertir las divisas
# Diccionario fijo de tasas de cambio (base USD)
tasas_cambio = {
    "USD": 1,
    "COP": 3999.59,
    "MXN": 18.72,
    "EUR": 0.86
}

#Metodo para convertir una moneda a otra usando el dolar como moneda tanto origen como destino
@app.route('/convertir', methods=['POST'])
def convertir_divisas():
    data = request.get_json() #Traemos el json que nos envian
    origen = data.get("origen") #Obtenemos la moneda origen
    destino = data.get("destino") #Obtenemos la moneda destino
    valor = data.get("valor") #Obtenemos la cantidad a convertir

    if not origen or not destino or valor is None: #Verificamos que los parametros no esten vacios
        return jsonify({"error": "Faltan parámetros"}), 400

    # Verificar si existe el registro en la base de datos
    conversion = divisas_collection.find_one({
        "origen": origen,
        "destino": destino
    })

    if not conversion: #Si no existe la conversion en la base de datos, retornamos un error
        return jsonify({"error": "Conversión no soportada en la base de datos"}), 400

    # Validar y calcular usando el diccionario de tasas
    try:
        cantidad = float(valor)
    except (TypeError, ValueError):
        return jsonify({"error": "Valor inválido"}), 400

    if origen not in tasas_cambio or destino not in tasas_cambio: #Verificamos que las monedas esten en el diccionario
        return jsonify({"error": "Moneda no soportada"}), 400

    tasa_origen = float(tasas_cambio[origen]) #Obtenemos la tasa de la moneda origen
    tasa_destino = float(tasas_cambio[destino]) #Obtenemos la tasa de la moneda destino
    tasa_efectiva = tasa_destino / tasa_origen #Calculamos la tasa efectiva
    equivalencia = cantidad * tasa_efectiva #Calculamos la equivalencia

    return jsonify({ #Retornamos el resultado de la conversion
        "origen": origen,
        "destino": destino,
        "cantidad": cantidad,
        "tasa": float(tasa_efectiva),
        "resultado": equivalencia
    }), 200