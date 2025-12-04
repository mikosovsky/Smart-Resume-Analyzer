# Upload, create-job, match endpoints
from fastapi import APIRouter, File, UploadFile
from backend.app.services.extract import PDFExtractor
from backend.app.services.resume_parser import ResumeParser

router = APIRouter()


@router.post("/resume/upload")
async def upload_resume(file: UploadFile = File(...)):
    pdf_extractor = PDFExtractor()
    if pdf_extractor.is_type(file.filename):
        resume_content = await pdf_extractor.extract_text(file)
        resume_parser = ResumeParser()
        parsed_resume = resume_parser.parse(resume_content)
        return parsed_resume
    return {"error": "Unsupported file type"}
