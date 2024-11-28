from pymongo import MongoClient

def get_db():
    client = MongoClient("mongodb://shared-db:27017/")
    return client.digital_replica
