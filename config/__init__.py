from flask import Flask
from flask_cors import CORS

def create_app():
    """Factory function to create the Flask app instance."""
    app = Flask(__name__)

    from resources.email_resource import email_bp

    CORS(app, resources={r"/api/*": {"origins": "https://andrelcarvalho.netlify.app"}}, allow_headers=["Content-Type"], supports_credentials=True)

    app.register_blueprint(email_bp)

    return app
