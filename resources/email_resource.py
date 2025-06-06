from flask import Blueprint, request, jsonify
from services.email_service import send_confirmation_email
from utils.response_http_util import standard_response

email_bp = Blueprint("email", __name__)

@email_bp.route('/email', methods=['POST', 'OPTIONS'])
def send_email():
    if request.method == 'OPTIONS':
        response = jsonify({"message": "CORS preflight successful"})
        response.headers.add("Access-Control-Allow-Origin", request.headers.get("Origin", "*"))
        response.headers.add("Access-Control-Allow-Headers", "Content-Type, Authorization")
        response.headers.add("Access-Control-Allow-Methods", "POST, OPTIONS")
        return response, 200

    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    title = data.get('title')
    message = data.get('message')

    if not email or not name or not message:
        return standard_response(False, "Invalid data", 400)

    try:
        send_confirmation_email(to_email=email, name=name, message=message, title=title)
        return standard_response(True, "E-mail enviado com sucesso", 200)
    except Exception as e:
        return standard_response(False, f"Erro: {str(e)}", 500)
