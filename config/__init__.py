import os
from flask import Flask
from flask_cors import CORS

def create_app():
    """Factory function to create the Flask app instance."""
    app = Flask(__name__)

    from resources.email_resource import email_bp

    cors_urls = os.getenv("CORS_URLS", "").split(",")
    cors_urls = [url.strip() for url in cors_urls if url]

    CORS(app, resources={r"/*": {"origins": cors_urls}},
         methods=["GET", "POST", "OPTIONS"],
         allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
         supports_credentials=True)

    app.register_blueprint(email_bp)

    return app

