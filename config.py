import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key')
    MONGO_URI = "mongodb+srv://swamy:ss1234455@cluster0.hcnfc.mongodb.net/Cluster0?retryWrites=true&w=majority&appName=Cluster0/"
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
