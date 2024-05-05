from pymongo import MongoClient
from config import CONFIG

MONGO_CLIENT = MongoClient(CONFIG.mongo_uri, serverSelectionTimeoutMS=60000)
