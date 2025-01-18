from langchain.tools import BaseTool
import boto3
from PIL import Image
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import uuid
import io
import os

load_dotenv(Path(__file__).parent.parent / '.env')

class ImageUploaderTool(BaseTool):
    name: str = "upload_image_to_s3_bucket"
    description: str = "Upload image to aws s3 bucket and return object url. Input should be an io.BytesIO object. Output should be a url string."

    def __init__(self):
        super().__init__()
        self.s3_client = boto3.client('s3')
        self.BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
        
    def upload_to_s3(self, image_content: io.BytesIO, original_filename: str) -> str:
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{timestamp}_{unique_id}_{original_filename}"
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.BUCKET_NAME,
                Key=filename,
                Body=image_content,
                ContentType='image/jpeg',
                ACL='public-read'
            )
            
            # Return public URL
            return f"https://{self.BUCKET_NAME}.s3.amazonaws.com/{filename}"
            
        except Exception as e:
            raise Exception(f"Failed to upload to S3: {str(e)}")

    def _run(self, content: io.BytesIO, filename: str) -> str:
        try:
            # Upload to S3
            public_url = self.upload_to_s3(content, filename)
            return public_url
        
        except Exception as e:
            return f"Error processing image: {str(e)}"