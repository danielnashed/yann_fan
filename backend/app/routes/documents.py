from fastapi import APIRouter, HTTPException, UploadFile, File
from fastapi.responses import JSONResponse
from typing import List
from app.agent.tools.vector_db_tool import VectorDBTool
from app.agent.tools.pdf_parser_tool import PDFParserTool
from app.agent.tools.docx_parser_tool import DOCXParserTool
from app.agent.tools.image_parser_tool import ImageParserTool
import uuid

router = APIRouter(prefix="/upload", tags=["Documents"])

# Upload new documents
@router.post("/{user_id}")
async def upload_files(
    user_id: str,
    files: List[UploadFile] = File(...)
    ):
    try:
        print('hello world')
        processed_files = []
        print('user ID: ', user_id)
        for file in files:
            id = user_id + '_'.join(file.filename.split()) +  '_' + str(uuid.uuid4())[:8]
            content = await file.read() # Read file content as bytes stream
            await file.seek(0)  # Reset file pointer
            # Process each file 
            if file.content_type == 'application/pdf':
                modality = 'text'
                text = PDFParserTool().run(content)
            elif file.content_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
                modality = 'text'
                text = DOCXParserTool().run(content)
            elif file.content_type.startswith('image/'):
                modality = 'image'
                filename = file.filename
                data = ImageParserTool().run(content, filename)
                url, text = data['url'], data['text'] # ignore text from image for now
            else:
                raise HTTPException(status_code=400, detail="Unsupported file type")
            # Add to processed files list
            processed_files.append({
                "id": id,
                "modality": modality,
                "url": url if file.content_type.startswith('image/') else None,
                "content": text,
            })
        # Upsert to vector database
        VectorDBTool().embed_and_upsert(processed_files)
            
        return JSONResponse(
            content={
                "message": "Files uploaded successfully",
                "files": processed_files
            },
            status_code=201
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

