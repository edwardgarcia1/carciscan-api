from typing import List, Dict, Any
from app.schemas.prediction import IngredientDetails  # Import for type hinting
from app.core.constants import ROUTE_ADVICE


def get_practical_advice(ingredient_results: List[IngredientDetails]) -> List[str]:
    """
    Aggregates practical advice from all predicted routes.
    """
    all_routes = set()
    for ing in ingredient_results:
        if ing.prediction_details:
            all_routes.update(ing.prediction_details.route_of_exposure)

    practical_advice_list = [ROUTE_ADVICE.get(route, "") for route in all_routes if ROUTE_ADVICE.get(route)]
    return practical_advice_list