from pymongo import MongoClient

MONGO_URL = "mongodb+srv://jyoti:RecallX@cluster0.skjdft0.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(MONGO_URL)

db = client["recallx"]

# Collections
memory_collection = db["memories"]
recording_collection = db["recordings"]