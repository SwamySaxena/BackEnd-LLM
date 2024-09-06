from flask import Flask
from extensions import mongo, bcrypt, jwt  # Import initialized objects
from config import Config
from flask_cors import CORS  # Import CORS

app = Flask(__name__)
app.config.from_object(Config)

# Enable CORS for all routes
CORS(app)

# Initialize the extensions with the app
try:
    mongo.init_app(app)
    print("MongoDB connection initialized successfully.")
except Exception as e:
    print(f"Error initializing MongoDB connection: {e}")

bcrypt.init_app(app)
jwt.init_app(app)

from routes.auth import auth_bp
from routes.conversation import conversation_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(conversation_bp, url_prefix='/api')

if __name__ == '__main__':
    app.run(debug=True)
