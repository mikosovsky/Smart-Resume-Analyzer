# PDF/DOCX → text; sectioning & chunking
from abc import ABC, abstractmethod
from fastapi import UploadFile
from fastapi.concurrency import run_in_threadpool
import fitz  # PyMuPDF


class DocumentExtractor(ABC):
    @abstractmethod
    def is_type(self, file_name: str) -> bool:
        pass

    @abstractmethod
    async def extract_text(self, upload_file: UploadFile) -> str:
        pass


class PDFExtractor(DocumentExtractor):
    def is_type(self, file_name: str) -> bool:
        return file_name.lower().endswith(".pdf")

    async def extract_text(self, upload_file: UploadFile) -> str:
        content = await upload_file.read()
        text = await run_in_threadpool(self._sync_extract, content)
        return text

    def _sync_extract(self, bytes_data: bytes) -> str:
        doc = fitz.open(stream=bytes_data, filetype="pdf")
        try:
            text = "".join(str(page.get_text()) for page in doc)
        finally:
            doc.close()
        return text


class TXTExtractor(DocumentExtractor):
    def is_type(self, file_name: str) -> bool:
        return file_name.lower().endswith(".txt")

    async def extract_text(self, upload_file: UploadFile) -> str:
        content = await upload_file.read()
        return content.decode("utf-8")
