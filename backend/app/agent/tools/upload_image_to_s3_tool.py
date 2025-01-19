from langchain.tools import BaseTool
import boto3
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
import uuid
import io
import os

load_dotenv()

# load_dotenv(Path(__file__).parent.parent.parent / '.env')

class ImageUploaderTool(BaseTool):
    name: str = "web_scraper"
    description: str = "Scrapes full content from a given URL"

    def _run(self, content: bytes, filename: str) -> str:
        try:
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('AWS_REGION')
            )

            BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            unique_id = str(uuid.uuid4())[:8]
            filename = f"{timestamp}_{unique_id}_{filename}"
            bytes_object = io.BytesIO(content)

            # Upload to S3
            s3_client.put_object(
                Bucket=BUCKET_NAME,
                Key=filename,
                Body=bytes_object,
                ContentType='image/jpeg',
            )

            return f"https://{BUCKET_NAME}.s3.amazonaws.com/{filename}"
        
        except Exception as e:
            return f"Error processing image: {str(e)}"
        




    # def __init__(self):
    #     super().__init__()
    #     self.name = "upload_image_to_s3_bucket"
    #     self.description = "Upload image to aws s3 bucket and return object url. Input should be an io.BytesIO object. Output should be a url string."
    #     aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID')
    #     aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    #     region_name =os.getenv('AWS_REGION')
    #     print('accessed env variables')
    #     print(aws_access_key_id, aws_secret_access_key, region_name)
    #     self.s3_client = boto3.client(
    #         's3',
    #         aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    #         aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    #         region_name=os.getenv('AWS_REGION')
    #     )
    #     print("Initialized S3 client.")
    #     self.BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
    #     print('bucket name: ', self.BUCKET_NAME)
        
    # def upload_to_s3(self, image_content: bytes, original_filename: str) -> str:
    #     try:
    #         bytes_object = io.BytesIO(image_content)
    #         # Generate unique filename
    #         timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    #         print('timestamp: ', timestamp)
    #         unique_id = str(uuid.uuid4())[:8]
    #         print('unique_id: ', unique_id)
    #         filename = f"{timestamp}_{unique_id}_{original_filename}"
    #         print('filename: ', filename)

    #         # Upload to S3
    #         self.s3_client.put_object(
    #             Bucket=self.BUCKET_NAME,
    #             Key=filename,
    #             Body=image_content,
    #             ContentType='image/jpeg',
    #             ACL='public-read'
    #         )
    #         print(f"Successfully uploaded {original_filename} to S3 bucket.")
            
    #         # Return public URL
    #         return f"https://{self.BUCKET_NAME}.s3.amazonaws.com/{filename}"
            
    #     except Exception as e:
    #         raise Exception(f"Failed to upload to S3: {str(e)}")