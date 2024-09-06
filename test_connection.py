from pymongo import MongoClient

# Use the standard connection string format
MONGO_URI = "mongodb+srv://swamy:ss1234455@cluster0.hcnfc.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
try:
    client = MongoClient(MONGO_URI)
    # Try to list databases
    databases = client.list_database_names()
    print("Successfully connected to MongoDB Atlas. Databases:", databases)
except Exception as e:
    print(f"Error connecting to MongoDB Atlas: {e}")
