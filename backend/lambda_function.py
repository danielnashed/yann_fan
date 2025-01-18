from app.main import app  # Import the FastAPI app
from mangum import Mangum # Connect the FastAPI app to Mangum

# Create the Lambda handler
handler = Mangum(app)