from fastapi.middleware.cors import CORSMiddleware

def setup_middleware(app):
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # Allows all origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
