from flask import Flask
from app.routes import main_blueprint

def create_app():
    """Create and configure the Flask app."""
    app = Flask(__name__)

    # Register the blueprint (API routes)
    app.register_blueprint(main_blueprint)

    return app
