from pymongo import MongoClient
import os
import redis

MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017")
# MongoDB
MONGO_URI = os.getenv("MONGO_URI")
mongo_client = MongoClient(MONGO_URI)
db = mongo_client.url_shortener
collection = db.urls

# Redis
redis_client = redis.Redis(
    host="redis",
    port=6379,
    decode_responses=True
)
