from fastapi import APIRouter, Query,Body
from controllers.fx_rates_controller import FxRatesController

router = APIRouter()

fx_rates_controller = FxRatesController()

@router.get("/latest", summary="Latest FX Rates")
def latest_fx_rates(
    currency: str = Query(..., description="Currency code, e.g., USD"),
):
    return fx_rates_controller.latest_fx_rates(currency)