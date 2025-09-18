from fastapi import APIRouter
from . import fx_rates_routes, metrcis_routes, news_routes

router = APIRouter()

router.include_router(fx_rates_routes.router, prefix="/fx-rates", tags=["FX Rates"])
router.include_router(metrcis_routes.router, prefix="/metrics", tags=["Company Financial Metrics"])
router.include_router(news_routes.router, prefix="/news", tags=["Company News"])



