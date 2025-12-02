from backend.app.services.extract import PDFExtractor
from fastapi import UploadFile
import io
import pytest


def create_upload_file(pdf_name) -> UploadFile:
    file_path = f"data/samples/{pdf_name}"
    with open(file_path, "rb") as f:
        file_content = f.read()
    upload_file = UploadFile(
        filename="sample_resume.pdf", file=io.BytesIO(file_content)
    )
    return upload_file


def txt_resume_content(txt_name) -> str:
    file_path = f"data/samples/{txt_name}"
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
        return content


@pytest.mark.parametrize(
    "pdf_name,txt_name",
    [
        ("resume_backend_engineer.pdf", "resume_backend_engineer.txt"),
        ("resume_frontend_engineer.pdf", "resume_frontend_engineer.txt"),
        ("resume_ml_engineer.pdf", "resume_ml_engineer.txt"),
    ],
)
@pytest.mark.asyncio
async def test_pdf_text_extraction(pdf_name, txt_name):
    upload_file = create_upload_file(pdf_name)
    pdf_extractor = PDFExtractor()
    extracted_text = await pdf_extractor.extract_text(upload_file)
    print(extracted_text)
    txt_resume = txt_resume_content(txt_name)
    assert txt_resume == extracted_text
