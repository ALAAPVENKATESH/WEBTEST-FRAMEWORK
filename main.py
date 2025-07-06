from flask import Flask
from app.routes import main
import os

# Use environment variable for secret key (best practice)
app = Flask(__name__, template_folder=os.path.join("app", "templates"))
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')  # Use a strong, unique value in production!

app.register_blueprint(main)

if __name__ == "__main__":
    app.run(debug=True)
