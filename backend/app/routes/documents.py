from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from app.agent.tools.vector_db_tool import embed_and_upsert
from app.agent.tools.pdf_parser_tool import PDFParserTool
from app.agent.tools.docx_parser_tool import DOCXParserTool
from app.agent.tools.image_parser_tool import ImageParserTool
from app.crud import UserCRUD
import uuid

router = APIRouter(prefix="/upload", tags=["Documents"])

# Upload new documents
@router.post("/{user_id}")
async def upload_files(
    user_id: str,
    files: List[UploadFile] = File(...)
    ):
    try:
        user = await UserCRUD.get_user_by_id(user_id) # get user object 
        processed_files = []
        print('user ID: ', user_id)
        print('type of user id: ', type(user_id))
        for file in files:
            clean_filename = '_'.join(file.filename.split())
            id = clean_filename +  '_' + str(uuid.uuid4())[:8]
            content = await file.read() # Read file content as bytes stream
            await file.seek(0)  # Reset file pointer
            print('file content type: ', file.content_type)
            # Process each file 
            if file.content_type == 'application/pdf':
                modality = 'text'
                chunks = PDFParserTool()._run(content)
            elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                modality = 'text'
                chunks = DOCXParserTool()._run(content)
            elif file.content_type.startswith('image/'):
                modality = 'image'
                data = ImageParserTool()._run(content=content, filename=clean_filename)
                print('image has been parsed and uploaded to s3 bucket.')
                # url, text = data['url'], data['text'] # ignore text from image for now
                chunks = [data['url']]
                print('url: ', chunks)
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
            # Add to processed files list
            for i, chunk in enumerate(chunks):
                processed_files.append({
                    "id": f"{id}_{i}",
                    "modality": modality,
                    "content": chunk,
                })
        # Upsert to vector database
        response = embed_and_upsert(inputs=processed_files, user_id=user.auto_increment_id)
        print('upserted to vector database. Done now.')
            
        return JSONResponse(
            content={
                "message": "Files uploaded successfully",
                "files": response
            },
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

