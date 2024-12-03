from flask import Flask
from flask_cors import CORS

def create_app(env='http://localhost:8080'):
    """Factory function to create the Flask app instance."""
    app = Flask(__name__)

    from resources.email_resource import email_bp

    CORS(app, resources={r"/email/*": {"origins": [env]}})

    app.register_blueprint(email_bp, url_prefix="/email")

    return app
