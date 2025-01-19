# Yann Fan LLM Agent

A RAG App for Yann LeCun fans out there! 

#### Check out deployed app at `https://yann-fan.vercel.app`

## Tech Stack

* FastAPI (for backend)
* Next.js (for frontend)
* TailwindCSS + daisyUI (for UI/UX)
* Docker (for building container images)
* AWS (for S3 + ECR + hosting backend as a serverless Lambda function)
* Vercel (for hosting frontend)
* LangChain + LangGraph (for agentic LLM framework)
* LangSmith (for agent tracing)
* Groq (for fast Llama3.1 model inference)
* Jina.ai (for embedding models)
* MongoDB (for noSQL database)
* Pinecone (for vector database)

## CI/CD
* Any pushes to prod branch will automatically build a docker image and push it to AWS ECR as well as deploy frontend to Vercel server.

## Backend

### Setup (on local machine)

1. Navigate to the backend directory:
    ```sh
    cd backend
    ```

2. Create a virtual environment:
    ```sh
    python3 -m venv .venv
    ```

3. Activate the virtual environment:
    ```sh
    source .venv/bin/activate
    ```

4. Install the dependencies:
    ```sh
    pip install -r requirements.txt
    ```

For the database, a free community version of MongoDB is used. Follow these instructions to download it:

1. Tap the MongoDB Homebrew Tap:
    ```sh
    brew tap mongodb/brew
    ```

2. Install MongoDB (free community edition):
    ```sh
    brew install mongodb-community@8.0
    ```

### Running the Database

1. Run as macOS service:
    ```sh
    brew services start mongodb-community@8.0
    ```

2. Run database migrations:
    ```sh
    python manage.py migrate
    ```

#### Visualizing the Database

1. Download MondoDB Compass from `https://www.mongodb.com/try/download/compass`
2. Add a connection using localhost url: `mongodb://localhost:27017`

### Running LocalStack for File Storage

1. Start Docker if it's not already running.
2. Start LocalStack:

   ```sh
   localstack start
   ```

### Running the Backend Server

1. Start the backend server:
    ```sh
    uvicorn app.main:app --reload
    ```

2. Access the backend: Open your browser and go to `http://localhost:8000`.

3. Checkout OpenAPI docs:
* Swagger UI: `http://127.0.0.1:8000/docs`
* ReDoc: `http://127.0.0.1:8000/redoc`


#### Tracing Agent with LangSmith

LangSmith can be used to trace the agent's behavior. This can be helpful for seeing which tools are called with what inputs/outputs.
Follow these steps to set up LangSmith:

1. Create an account on LangSmith: `https://smith.langchain.com/` and generate an API key.
2. Add the following to your .bashrc/.zshrc file and restart the terminal:

    ```sh
    export LANGCHAIN_TRACING_V2=true
    export LANGCHAIN_PROJECT=job-search-llm-agent
    export LANGCHAIN_API_KEY=<your api key>
    ```

3. Run the backend server like normal
4. When the agent is called, traces will be sent to LangSmith automatically

## Frontend

### Setup (on local machine)

1. Navigate to the frontend directory:
    ```sh
    cd frontend
    ```

2. Install the dependencies:
    ```sh
    npm install
    ```

### Running the Frontend

1. Start the frontend development server:
    ```sh
    npm run dev
    ```

2. Access the frontend: Open your browser and go to `http://localhost:3000`.


## Environment Variables

Copy the `.env.example` file in the root directory to `.env` and add the necessary environment variables for both the backend and frontend.

## Contributing

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some feature'`).
5. Push to the branch (`git push origin feature-branch`).
6. Open a pull request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.