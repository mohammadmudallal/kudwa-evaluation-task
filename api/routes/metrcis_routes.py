from fastapi import APIRouter, Query,Body
from controllers.metrics_controller import MetricsController

router = APIRouter()

metrics_controller = MetricsController()

@router.get("/", summary="Company Financial Metrics")
def latest_metrics(
    company_id: str = Query(..., description="Comapny"),

):
    return metrics_controller.get_company_metrics(company_id)

@router.get("/annual", summary="Company Annual Financial Metrics")
def latest_metrics(
    company_id: str = Query(..., description="Comapny"),
    from_year: str = Query(..., description="Year From"),
    to_year: str = Query(..., description="Year To"),

):
    return metrics_controller.get_company_annaul_metrics(company_id, from_year, to_year)

@router.get("/quarterly", summary="Company Quarterly Financial Metrics")
def latest_metrics(
    company_id: str = Query(..., description="Comapny"),
    from_year: str = Query(..., description="Year From"),
    to_year: str = Query(..., description="Year To"),

):
    return metrics_controller.get_company_quartely_metrics(company_id, from_year, to_year)