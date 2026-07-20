import os
from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))

db = client["NeuroLearn"]

chat_history = db["chat_history"]
eeg_history = db["eeg_history"]
learning_progress = db["learning_progress"]