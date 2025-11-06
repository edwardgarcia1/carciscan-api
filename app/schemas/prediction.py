from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# --- Schemas for Individual Ingredients ---
class PredictionDetails(BaseModel):
    carcinogenicity_group: Optional[str]
    evidence: Optional[str]
    confidence: Optional[float] = Field(..., ge=0, le=100, description="Confidence percentage from 0 to 100.")
    route_of_exposure: List[str]

class IngredientDetails(BaseModel):
    name: str
    prediction_details: Optional[PredictionDetails]
    matched_name: Optional[str]
    pubchem_url: Optional[str]
    status: Optional[str] = Field(..., description="Status of processing, e.g., 'Success', 'Synonym not found'")

# --- Schemas for the Overall Response ---
class OcrResult(BaseModel):
    text: str
    ingredients: List[str]

# The CallToAction schema is no longer needed, as we are removing it.

class PredictionResponse(BaseModel):
    success: bool
    message: str
    ocr_result: Optional[OcrResult]
    ingredients: List[IngredientDetails]
    processing_time: float
    practical_advice: List[str]