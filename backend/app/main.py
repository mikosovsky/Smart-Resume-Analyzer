from fastapi import FastAPI
from .api.routes import router

app = FastAPI()

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
