# Upload, create-job, match endpoints
from fastapi import APIRouter, File, UploadFile
from backend.app.services.extract import PDFExtractor, TXTExtractor
from backend.app.services.resume_parser import ResumeParser
from backend.app.services.jd_parser import JobDescriptionParser
from backend.app.services.explain import ExplanationService

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


@router.post("/job-description/upload")
async def upload_job_description(file: UploadFile = File(...)):
    txt_extractor = TXTExtractor()
    if txt_extractor.is_type(file.filename):
        jd_content = await txt_extractor.extract_text(file)
        jd_parser = JobDescriptionParser()
        parsed_jd = jd_parser.parse(jd_content)
        return parsed_jd
    return {"error": "Unsupported file type"}


@router.post("/match")
async def match_resume_to_jd(
    resume_file: UploadFile = File(...), jd_file: UploadFile = File(...)
):
    pdf_extractor = PDFExtractor()
    txt_extractor = TXTExtractor()

    if not pdf_extractor.is_type(resume_file.filename):
        return {"error": "Unsupported resume file type"}
    if not txt_extractor.is_type(jd_file.filename):
        return {"error": "Unsupported job description file type"}

    resume_content = await pdf_extractor.extract_text(resume_file)
    jd_content = await txt_extractor.extract_text(jd_file)

    resume_parser = ResumeParser()
    jd_parser = JobDescriptionParser()

    parsed_resume = resume_parser.parse(resume_content)
    parsed_jd = jd_parser.parse(jd_content)

    explanation_service = ExplanationService()
    explanation = explanation_service.explain_match(parsed_resume, parsed_jd)

    return explanation
