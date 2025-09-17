from fastapi import FastAPI
from routes import index as routes  # Import index router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="Kudwa Evaluation Test", version="1.0.0")

app.include_router(routes.router, prefix="/api")

origins = [
    "http://localhost:3001",   # Next.js local dev
    "http://51.77.157.52:3001", # add production URL when deployed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],            # allow all HTTP methods
    allow_headers=["*"],            # allow all headers
)

if __name__ == "__main__":
    uvicorn.run(
        "server:app",  # file_name:FastAPI_instance
        host="0.0.0.0",
        port=8000,
        reload=True
    )

