
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from networksecurity.components.constants import MONGO_DB_URI

# Replace the uri string with your MongoDB deployment's connection string.
uri = MONGO_DB_URI

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)