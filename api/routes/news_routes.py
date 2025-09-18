from fastapi import APIRouter, Query,Body
from controllers.news_controller import NewsController

router = APIRouter()

news_controller = NewsController()

@router.get("/", summary="Latest News")
def latest_news(
    company_id: str = Query(..., description="Comapny"),
    days: str = Query(..., description="Days"),
):
    return news_controller.latest_news(company_id, days)