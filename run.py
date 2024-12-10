import os
from app import create_app
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()

if __name__ == "__main__":
    # Get the port from the PORT environment variable, defaulting to 5000 for local development
    port = int(os.environ.get("PORT", 5000))
    
    # Check the environment type (default to 'development')
    env = os.environ.get("ENV", "development")

    if env == "production":
        # For production, use Gunicorn
        from gunicorn.app.base import BaseApplication

        class GunicornApp(BaseApplication):
            def __init__(self, app, options=None):
                self.application = app
                self.options = options or {}
                super().__init__()

            def load_config(self):
                for key, value in self.options.items():
                    self.cfg.set(key, value)

            def load(self):
                return self.application

        options = {
            'bind': f'0.0.0.0:{port}',
            'workers': 2,  # Adjust based on platform limits
            'threads': 4,
            'timeout': 120
        }
        GunicornApp(app, options).run()
    else:
        # For local development, use Flask's built-in server
        app.run(host="0.0.0.0", port=port, debug=True)
