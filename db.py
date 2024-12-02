from pymongo import MongoClient
import os

def get_db():
    mongo_uri = os.getenv("MONGO_URI", "mongodb://localhost:27017/")  # Default to localhost
    client = MongoClient(mongo_uri)
    return client.digital_replica
