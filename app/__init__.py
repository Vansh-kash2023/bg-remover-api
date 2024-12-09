from flask import Flask

def create_app():
    app = Flask(__name__)

    # Register Blueprints (modular structure)
    from app.routes import main
    app.register_blueprint(main)

    return app
