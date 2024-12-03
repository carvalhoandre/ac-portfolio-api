from flask import Blueprint, request
from services.email_service import EmailService
from utils.response_http_util import standard_response

email_bp = Blueprint("email", __name__)
email_service = EmailService()

@email_bp.route('/send', methods=['POST'])
def send_email():
    data = request.get_json()
    email = data.get('email')
    name = data.get('name')
    title = data.get('title')
    message = data.get('message')

    if not email or not name or not message:
        return standard_response(False, "Invalid data", 400)

    try:
        email_service.send_confirmation_email(to_email=email, name=name, message=message, title=title)
        return standard_response(True, "E-mail enviado com sucesso", 200)
    except Exception as e:
        return standard_response(False, f"Erro: {str(e)}", 500)
