from fastapi import APIRouter
from app.api.v1.endpoints import predictions

api_router = APIRouter()

# Include the router from the predictions endpoint
# The prefix /predict will be added to the main API_V1_STR prefix
api_router.include_router(predictions.router, prefix="/predict", tags=["predictions"])