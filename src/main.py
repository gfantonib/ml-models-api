import uvicorn
from fastapi import FastAPI

from src.api.v1.ant_colony_router import router as ant_colony_router

app = FastAPI()

app.include_router(ant_colony_router, prefix="/v1")


@app.get("/")
def read_root():
    return {"message": "ml-models-api is online!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
