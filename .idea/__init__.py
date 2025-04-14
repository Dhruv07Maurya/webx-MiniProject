from flask import Flask
from flask_cors import CORS
from pymongo import MongoClient
from dotenv import load_dotenv
import os
import cloudinary

# Load environment variables from .env
load_dotenv()

# MongoDB setup
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "WEBX_MINIPROJECT")

# Initialize Mongo client and connect to the specific DB
client = MongoClient(MONGO_URI)
mongo = client[DB_NAME]

# ✅ Cloudinary setup
CLOUDINARY_URL = os.getenv("CLOUDINARY_URL")

if CLOUDINARY_URL:
    try:
        cloudinary.config(cloudinary_url=CLOUDINARY_URL)
    except Exception as e:
        print(f"❌ Error configuring Cloudinary: {e}")
else:
    print("❌ CLOUDINARY_URL not found in environment variables!")

def create_app():
    app = Flask(__name__)

    # Secret key for session security
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")

    # ✅ CORS Configuration
    CORS(app,
         supports_credentials=True,
         resources={r"/api/*": {"origins": "http://localhost:5173"}})

    # Attach mongo connection to app instance for use in routes
    app.mongo = mongo

    # Import and register routes
    from .routes.auth_routes import auth_bp
    from .routes.post_routes import post_bp

    app.register_blueprint(auth_bp, url_prefix='/api')
    app.register_blueprint(post_bp, url_prefix='/api')

    return app