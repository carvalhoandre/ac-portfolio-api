import os
from config import create_app
from dotenv import load_dotenv

load_dotenv()

env = os.getenv('CORS_URL_ENV', 'http://localhost:8080')

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
