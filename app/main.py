from fastapi import FastAPI
from app.core.config import settings
from app.api.v1.api import api_router

# Create the FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Include the main API router
app.include_router(api_router, prefix=settings.API_V1_STR)

# A simple root endpoint to check if the API is running
@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Welcome to the Carciscan API. See /docs for the API documentation."}
