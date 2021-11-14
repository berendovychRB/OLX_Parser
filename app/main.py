from fastapi import FastAPI

from app.endpoints import routers

app = FastAPI()

app.include_router(routers.router)


@app.get("/")
async def root():
    return {"message": "Project Starting"}
