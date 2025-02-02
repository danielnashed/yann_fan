from fastapi import FastAPI
from app.routes import users, conversations, documents
from app.middleware import setup_middleware
from app.db import init as init_db
import requests
from requests.exceptions import RequestException
from dotenv import load_dotenv
import os
from phoenix.otel import register
from openinference.instrumentation.langchain import LangChainInstrumentor


load_dotenv()

# Function to check for network connectivity
def check_network_connectivity():
    test_url = "https://httpbin.org/get"  # Using a public endpoint for the test
    try:
        response = requests.get(test_url, timeout=5)  # 5 seconds timeout for the test
        if response.status_code == 200:
            print("Network connectivity test passed.")
        else:
            raise Exception(f"Network connectivity test failed with status code: {response.status_code}")
    except RequestException as e:
        print(f"Error: Network connectivity test failed. Exception: {str(e)}")
        raise e

# Perform network connectivity check on Lambda startup
check_network_connectivity()

app = FastAPI(title="My Backend API")

setup_middleware(app)
app.include_router(conversations.router)
app.include_router(users.router)
app.include_router(documents.router)

# Add Phoenix API Key for tracing
PHOENIX_API_KEY = os.getenv("PHOENIX_API_KEY")
print("Phoenix API Key: ", PHOENIX_API_KEY)
os.environ["PHOENIX_CLIENT_HEADERS"] = f"api_key={PHOENIX_API_KEY}"
os.environ["PHOENIX_COLLECTOR_ENDPOINT"] = "https://app.phoenix.arize.com"


@app.on_event("startup")
async def on_startup():
    await init_db()  # Initialize the database and Beanie

    # Configure the Phoenix tracer
    tracer_provider = register(
        project_name="my-llm-app", 
        ) 
    print("Phoenix tracer initialized")

    # Instrument LangChain
    LangChainInstrumentor().instrument(tracer_provider=tracer_provider)
    print("LangChain instrumented")


@app.on_event("shutdown")
async def on_shutdown():
    # Stop Phoenix tracer
    # tracer_provider.stop() ???
    print('Shutting down backend')


@app.get("/")
def read_root():
    return {"message": "Welcome to my Backend API!"}