# db.py
import motor.motor_asyncio
from beanie import init_beanie
from dotenv import load_dotenv
import os
from pathlib import Path

# Load environment variables from .env file
load_dotenv(Path(__file__).parent.parent / '.env')

# MongoDB Atlas connection URI from environment variable
connection_string = os.getenv("MONGODB_URI")

# MongoDB connection URI
client = motor.motor_asyncio.AsyncIOMotorClient(connection_string)
database = client["mydatabase"]

# Beanie initialization
async def init():
    # Initialize Beanie with the database and all the document models
    await init_beanie(database, document_models=[])


# Function to get the next sequence value
async def get_next_sequence_value(sequence_name: str) -> int:
    counter = await database.counters.find_one_and_update(
        {"_id": sequence_name},
        {"$inc": {"sequence_value": 1}},
        upsert=True,
        return_document=True
    )
    return counter["sequence_value"]