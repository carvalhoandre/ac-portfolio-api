# config/__init__.py

from flask import Flask

def create_app():
    """Factory function to create the Flask app instance."""
    app = Flask(__name__)

    from resources.email_resource import email_bp

    app.register_blueprint(email_bp)

    return app
