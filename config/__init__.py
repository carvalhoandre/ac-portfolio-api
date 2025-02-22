from os import getenv
from flask import Flask
from flask_cors import CORS

def create_app():
    """Factory function to create the Flask app instance."""
    app = Flask(__name__)

    from resources.email_resource import email_bp

    allowed_origins = [
        "https://www.andreleitecarvalho.space",
        "https://andrelcarvalho.netlify.app"
    ]

    CORS(app, resources={r"/*": {"origins": allowed_origins}},
         methods=["GET", "POST", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         supports_credentials=True)

    app.register_blueprint(email_bp)

    return app
