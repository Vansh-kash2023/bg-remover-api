import os
from app import create_app
from dotenv import load_dotenv

load_dotenv()
app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    env = os.environ.get("ENV", "development")

    if env == "production":
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
            'workers': 2,
            'threads': 4,
            'timeout': 120
        }
        GunicornApp(app, options).run()
    else:
        app.run(host="0.0.0.0", port=port, debug=True)
