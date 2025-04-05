from fastapi import FastAPI
from .controllers import auth_controllers
from fastapi.middleware.cors import CORSMiddleware
from .utils.handler_logging import setup_logging
# from app.controllers.example_controller import router as example_router

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or "*"
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Setup logging
setup_logging()

# Include routers
# app.include_router(example_router, prefix="/api/v1")
app.include_router(auth_controllers.router, prefix="/api/v1/auth", tags=["auth"])

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.get("/health")
async def health_check():
    return {"status":"OK"}