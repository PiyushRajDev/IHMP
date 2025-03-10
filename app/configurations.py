from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://Piyush:<Pi122912>@ihmp.a3xgm.mongodb.net/?retryWrites=true&w=majority&appName=IHMP"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

