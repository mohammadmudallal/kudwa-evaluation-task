from fastapi import FastAPI
from routes import index as routes  # Import index router
import uvicorn

app = FastAPI(title="Kudwa Evaluation Test", version="1.0.0")

app.include_router(routes.router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "server:app",  # file_name:FastAPI_instance
        host="0.0.0.0",
        port=5000,
        reload=True
    )

