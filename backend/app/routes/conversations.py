from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from app.crud import ConversationCRUD as CRUD

router = APIRouter(prefix="/conversations", tags=["Conversations"])

class ConversationRequest(BaseModel):
    user_id: str

class UpdateConversationRequest(BaseModel):
    user_id: str
    message: str

# Create a new Conversation
@router.post("/")
async def create_conversation_route(request: ConversationRequest):
    new_conversation = await CRUD.create_conversation(request.user_id)
    return JSONResponse(content={"conv_id": str(new_conversation.id)}, 
                        status_code=201)

# Get a Conversation by ID
@router.get("/{conv_id}")
async def get_conversation_route(conv_id: str, request: ConversationRequest):
    conversation = await CRUD.get_conversation_by_id(conv_id, request.user_id)
    if not conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conversation

# Get all Conversations
@router.get("/")
async def get_conversation_route(request: ConversationRequest):
    conversations = await CRUD.get_all_conversations_by_user_id(request.user_id)
    if not conversations:
        raise HTTPException(status_code=404, detail="Conversations not found")
    return conversations

# Update a Conversation
@router.put("/{conv_id}")
async def update_conversation_route(conv_id: str, request: UpdateConversationRequest):
    updated_conversation = await CRUD.update_conversation(conv_id, request.user_id, request.message)
    if not updated_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return JSONResponse(content={"message": updated_conversation.graph_state["messages"][-1]["data"]["content"]}, 
                        status_code=200)

# Delete a Conversation
@router.delete("/{conv_id}")
async def delete_conversation_route(conv_id: str, request: ConversationRequest):
    result = await CRUD.delete_conversation(conv_id, request.user_id)
    if result.get("message") == "Conversation not found":
        raise HTTPException(status_code=404, detail="Conversation not found")
    return JSONResponse(content=result, 
                        status_code=200)