from pydantic import BaseModel
from beanie import Document
from typing import Dict
from datetime import datetime

class Conversation(BaseModel):
    user_id: str
    graph_state: Dict = {}  # Default value is an empty dict
    created_at: datetime = None
    updated_at: datetime = None

class ConversationDocument(Conversation, Document):
    pass
    class Settings:
        name = "conversations"  # MongoDB collection name

class User(BaseModel):
    auto_increment_id: int
    created_at: datetime = None  # Automatically set when a user is created

class UserDocument(User, Document):
    auto_increment_id: int
    created_at: datetime
    class Settings:
        name = "users"  # MongoDB collection name
