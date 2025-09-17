from fastapi import APIRouter, Query,Body
from controllers.test_controller import TestController

router = APIRouter()

test_controller = TestController()

@router.get("/test", summary="Test API")
def test(
    # imsi: str = Query(..., description="IMSI number to search"),
    # start_time: str = Query(..., description="Start time in format YYYY-MM-DD HH:MM:SS"),
    # end_time: str = Query(..., description="End time in format YYYY-MM-DD HH:MM:SS"),
    # window: int = Query(60, description="Window size in seconds for session grouping")
):
    return test_controller.test()