from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.crud import UserCRUD as CRUD

router = APIRouter(prefix="/users", tags=["Users"])

# Create a new User
@router.post("/")
async def create_user_route():
    new_user = await CRUD.create_user()
    return JSONResponse(content={"user_id": str(new_user.id)}, 
                        status_code=201)

# Get a User by ID
@router.get("/{user_id}")
async def get_user_route(user_id: str):
    user = await CRUD.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content={"user_id": str(user.id)}, 
                        status_code=200)

# Delete a User
@router.delete("/{user_id}")
async def delete_user_route(user_id: str):
    result = await CRUD.delete_user(user_id)
    if result.get("message") == "User not found":
        raise HTTPException(status_code=404, detail="User not found")
    return JSONResponse(content=result, 
                        status_code=200)