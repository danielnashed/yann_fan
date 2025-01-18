# conversation_crud.py
from datetime import datetime
from typing import Optional, List
from .models import ConversationDocument, UserDocument
from fastapi import HTTPException
from bson import ObjectId
from .db import get_next_sequence_value


class UserCRUD():
    # Create a new user
    @staticmethod
    async def create_user() -> UserDocument:
        auto_increment_id = await get_next_sequence_value("user_id")
        new_user = UserDocument(auto_increment_id=auto_increment_id,
                                created_at=datetime.now())
        await new_user.insert()
        return new_user
    
    # Get a user by ID
    @staticmethod
    async def get_user_by_id(user_id: str) -> Optional[UserDocument]:
        return await UserDocument.find_one({"_id": ObjectId(user_id)})
    
    # Delete a user by ID
    @staticmethod
    async def delete_user(user_id: str) -> dict:
        existing_user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if existing_user:
            await existing_user.delete()
            return {"message": "User deleted"}
        return {"message": "User not found"}
