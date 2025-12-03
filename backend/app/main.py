from fastapi import FastAPI
from .api.routes import router
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.include_router(router)


@app.get("/health")
async def health_check():
    return {"status": "ok"}
