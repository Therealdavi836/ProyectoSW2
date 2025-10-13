# Microservicio universal de reportes (PDF y Excel)
from flask import Flask, request, send_file, jsonify
from reports.pdf_report import generate_pdf
from reports.excel_report import generate_excel
import requests
import tempfile
import os

app = Flask(__name__)

def get_data_from_ms(ms_url, token):
    """
    Consulta datos desde cualquier microservicio, usando autenticación Bearer.
    """
    headers = {"Authorization": f"Bearer {token}"}
    try:
        response = requests.get(ms_url, headers=headers, timeout=10)
        response.raise_for_status()
        data = response.json()
        if not data:
            raise ValueError("El microservicio no devolvió datos")
        return data
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Error al conectar con {ms_url}: {str(e)}")
    except ValueError as e:
        raise RuntimeError(str(e))

@app.route("/report/pdf", methods=["POST"])
def report_pdf():
    """
    Genera un reporte PDF dinámico a partir de datos obtenidos desde otro microservicio.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401

    ms_url = request.json.get("ms_url")
    report_type = request.json.get("type", "general")

    if not ms_url:
        return jsonify({"error": "ms_url no proporcionado"}), 400

    try:
        data = get_data_from_ms(ms_url, token)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
        filename = generate_pdf(data, filename=tmp_file.name)
        download_name = f"reporte_{report_type}.pdf"

        return send_file(filename, as_attachment=True, download_name=download_name, mimetype="application/pdf")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/report/excel", methods=["POST"])
def report_excel():
    """
    Genera un reporte Excel dinámico a partir de datos obtenidos desde otro microservicio.
    """
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        return jsonify({"error": "Token no proporcionado"}), 401

    ms_url = request.json.get("ms_url")
    report_type = request.json.get("type", "general")

    if not ms_url:
        return jsonify({"error": "ms_url no proporcionado"}), 400

    try:
        data = get_data_from_ms(ms_url, token)
        tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx")
        filename = generate_excel(data, filename=tmp_file.name)
        download_name = f"reporte_{report_type}.xlsx"

        return send_file(filename, as_attachment=True, download_name=download_name,
                         mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/report/health", methods=["GET"])
def health_check():
    """
    Verifica que el microservicio de reportes esté activo.
    """
    return jsonify({
        "status": "ok",
        "service": "Microservicio de Reportes",
        "version": "1.0",
        "description": "Servicio Flask que genera reportes en PDF y Excel."
    }), 200


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)