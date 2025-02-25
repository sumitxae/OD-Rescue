from fastapi import FastAPI
# from app.controllers.example_controller import router as example_router

app = FastAPI()

# Include routers
# app.include_router(example_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Welcome to FastAPI"}

@app.get("/health")
async def health_check():
    return {"status":"OK"}