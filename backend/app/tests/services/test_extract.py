from backend.app.services.extract import PDFExtractor
from fastapi import UploadFile
import io
import pytest


@pytest.fixture
def create_upload_file() -> UploadFile:
    file_path = "data/samples/resume_backend_engineer.pdf"
    with open(file_path, "rb") as f:
        file_content = f.read()
    upload_file = UploadFile(
        filename="sample_resume.pdf", file=io.BytesIO(file_content)
    )
    return upload_file


@pytest.fixture
def txt_resume_content() -> str:
    file_path = "data/samples/resume_backend_engineer.txt"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return content


@pytest.mark.asyncio
async def test_pdf_text_extraction(create_upload_file, txt_resume_content):
    upload_file = create_upload_file
    pdf_extractor = PDFExtractor()
    extracted_text = await pdf_extractor.extract_text(upload_file)
    txt_resume = txt_resume_content
    assert txt_resume == extracted_text
