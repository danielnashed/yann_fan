from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/upload", tags=["Documents"])

# class DocumentRequest(BaseModel):
#     user_id: str

# Upload new documents
@router.post("/{user_id}")
async def upload_files(
    user_id: str,
    files: List[UploadFile] = File(...)
    ):
    try:
        print('hello world')
        uploaded_files = []
        print('user ID: ', user_id)
        for file in files:
            # Process each file
            file_info = {
                "filename": file.filename,
                "content_type": file.content_type,
                "size": file.size,
                "user_id": user_id
            }
            await file.seek(0)  # Reset file pointer
            uploaded_files.append(file_info)
            
        return JSONResponse(
            content={
                "message": "Files uploaded successfully",
                "files": uploaded_files
            },
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

