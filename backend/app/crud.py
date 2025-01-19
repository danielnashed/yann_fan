from datetime import datetime
from typing import Optional, List
from .models import ConversationDocument, UserDocument
from fastapi import HTTPException
from bson import ObjectId
from .agent.llm_agent import ChatAgent
# from .agent.agent import ChatAgent
from .db import get_next_sequence_value

class ConversationCRUD():
    # Create a new Conversation
    @staticmethod
    async def create_conversation(user_id: str) -> ConversationDocument:
        # Ensure the user exists
        user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        conv = ConversationDocument(user_id=user_id, 
                                    graph_state={}, 
                                    created_at=datetime.now(), 
                                    updated_at=datetime.now())
        await conv.insert()
        return conv

    # Get a Conversation by ID for a specific user
    @staticmethod
    async def get_conversation_by_id(conv_id: str, user_id: str) -> Optional[ConversationDocument]:
        return await ConversationDocument.find_one({"_id": ObjectId(conv_id), "user_id": user_id})

    # Get all Conversations for a specific user
    @staticmethod
    async def get_all_conversations_by_user_id(user_id: str) -> List[ConversationDocument]:
        return await ConversationDocument.find({"user_id": user_id}).to_list()

    # Update a Conversation for a specific user
    @staticmethod
    async def update_conversation(conv_id: str, user_id: str, message: str) -> Optional[ConversationDocument]:
        conv = await ConversationCRUD.get_conversation_by_id(conv_id, user_id)
        user = await UserCRUD.get_user_by_id(ObjectId(user_id))
        if conv:
            chat_agent = ChatAgent(user_id=user.auto_increment_id) # create agent
            # Process message with LangGraph agent
            state = chat_agent.deserialize_state(
                conv.graph_state
            )
            agent_result = chat_agent.process_user_message(
                message,
                state,
            )
            # Update graph state
            conv.graph_state = chat_agent.serialize_state(
                agent_result['state'])
            conv.updated_at = datetime.now()
            await conv.save()
        return conv

    # Delete a Conversation for a specific user
    @staticmethod
    async def delete_conversation(conv_id: str, user_id: str) -> dict:
        conv = await ConversationCRUD.get_conversation_by_id(conv_id, user_id)
        if conv:
            await conv.delete()
            return {"message": "Conversation deleted"}
        return {"message": "Conversation not found"}


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
