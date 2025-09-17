import pandas as pd
from fastapi import HTTPException, Response

class TestController:
    def __init__(self):
        pass
        
    def test(self):
        try:
            return Response(content="Test")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))