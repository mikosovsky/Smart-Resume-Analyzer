# Upload, create-job, match endpoints
from fastapi import APIRouter, File, UploadFile

router = APIRouter()


@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    return {"status": "ok"}
