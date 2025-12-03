from backend.app.services.extract import PDFExtractor, TXTExtractor
from fastapi import UploadFile
import io
import pytest


def create_pdf_upload_file(pdf_name) -> UploadFile:
    file_path = f"data/samples/{pdf_name}"
    with open(file_path, "rb") as f:
        file_content = f.read()
    upload_file = UploadFile(
        filename="sample_resume.pdf", file=io.BytesIO(file_content)
    )
    return upload_file


def create_txt_upload_file(txt_name) -> UploadFile:
    file_path = f"data/samples/{txt_name}"
    content = ""
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    upload_file = UploadFile(
        filename="sample_resume.txt", file=io.BytesIO(content.encode("utf-8"))
    )
    return upload_file


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
    upload_file = create_pdf_upload_file(pdf_name)
    pdf_extractor = PDFExtractor()
    extracted_text = await pdf_extractor.extract_text(upload_file)
    print(extracted_text)
    txt_upload_file = create_txt_upload_file(txt_name)
    txt_extractor = TXTExtractor()
    expected_text = await txt_extractor.extract_text(txt_upload_file)
    assert expected_text == extracted_text
