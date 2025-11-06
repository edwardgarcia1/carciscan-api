import sys
import os

# Add the project root to the Python path to allow imports from 'app'
# This is a bit of a hack for running the script directly, but it works.
# In a real deployment, the app would be run as a module.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

import time
from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session

# Import all our services and schemas
from app.services.ocr import extract_text_from_image
from app.services.parser import parse_ingredients
from app.crud.carciscan import get_cid_by_synonym, get_smiles_by_cid
from app.services.descriptors import calculate_rdkit_descriptors
from app.services.predictor import predict_carcinogenicity, predict_route
from app.services.analyzer import get_practical_advice
from app.services.matcher import find_best_synonym_match
from app.api.deps import get_db

from app.schemas.prediction import (
    PredictionResponse, IngredientDetails, PredictionDetails, OcrResult
)
from app.core.constants import IARC_EVIDENCE

router = APIRouter()


@router.post("/predict", response_model=PredictionResponse)
async def predict_from_image(
        file: UploadFile = File(...),
        db: Session = Depends(get_db)
):
    start_time = time.time()

    # 1. OCR
    try:
        image_bytes = await file.read()
        raw_text = extract_text_from_image(image_bytes)
        if not raw_text:
            raise HTTPException(status_code=400, detail="Could not extract text from the image.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during image processing: {e}")

    # 2. Parsing
    ingredient_names = parse_ingredients(raw_text)
    if not ingredient_names:
        raise HTTPException(status_code=400, detail="Could not parse any ingredients from the extracted text.")

    ocr_result = OcrResult(text=raw_text, ingredients=ingredient_names)

    # 3. Loop through ingredients and process each one
    final_ingredient_details = []
    for name in ingredient_names:
        print(f"--- Processing ingredient: {name} ---")

        # 4. Fuzzy Lookup for CID and Matched Name
        match_result = find_best_synonym_match(name, db)

        if not match_result:
            final_ingredient_details.append(
                IngredientDetails(
                    name=name,
                    prediction_details=None,
                    matched_name=None,
                    pubchem_url=None,
                    status="Synonym not found in database"
                )
            )
            continue

        # Unpack the result
        matched_name, cid = match_result
        print(f"Fuzzy match found: '{name}' -> '{matched_name}' with CID {cid}")

        # 5. Lookup SMILES
        smiles = get_smiles_by_cid(db, cid)
        if not smiles:
            final_ingredient_details.append(
                IngredientDetails(
                    name=name,
                    prediction_details=None,
                    matched_name=matched_name,
                    pubchem_url=None,
                    status="SMILES not found in database"
                )
            )
            continue

        # 6. Calculate Descriptors
        descriptor_dict = calculate_rdkit_descriptors(smiles)
        if not descriptor_dict:
            final_ingredient_details.append(
                IngredientDetails(
                    name=name,
                    prediction_details=None,
                    matched_name=matched_name,
                    pubchem_url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                    status="Could not calculate molecular descriptors"
                )
            )
            continue

        # 7. Predict
        carc_pred_dict = predict_carcinogenicity(descriptor_dict)
        route_pred_dict = predict_route(descriptor_dict)

        # 8. Structure the result for this ingredient
        prediction_details = None
        if carc_pred_dict and route_pred_dict:
            predicted_group = carc_pred_dict.get("prediction")
            raw_confidence = carc_pred_dict.get("confidence_scores", {}).get(predicted_group, 0)
            formatted_confidence = f"{raw_confidence * 100:.2f}"

            prediction_details = PredictionDetails(
                carcinogenicity_group=predicted_group,
                evidence=carc_pred_dict.get("evidence"),
                confidence=formatted_confidence,
                route_of_exposure=route_pred_dict.get("prediction", [])
            )
            status = "Success"
        else:
            status = "Prediction model failed"

        final_ingredient_details.append(
            IngredientDetails(
                name=name,
                prediction_details=prediction_details,
                matched_name=matched_name,
                pubchem_url=f"https://pubchem.ncbi.nlm.nih.gov/compound/{cid}",
                status=status
            )
        )

    # 9. Get practical advice
    practical_advice = get_practical_advice(final_ingredient_details)

    # 10. Calculate processing time and return response
    processing_time = round(time.time() - start_time, 2)

    return PredictionResponse(
        success=True,
        message="Analysis complete.",
        ocr_result=ocr_result,
        ingredients=final_ingredient_details,
        processing_time=processing_time,
        practical_advice=practical_advice
    )