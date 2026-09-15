import os
import io
import PyPDF2
import docx
from typing import Dict, Any, Tuple

class ResumeParser:
    """
    Handles file validation and text extraction for PDF and DOCX resume files.
    """
    
    ALLOWED_EXTENSIONS = {".pdf", ".docx"}
    MAX_FILE_SIZE_MB = 5
    MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024
    
    def __init__(self, file_path_or_bytes: Any, filename: str) -> None:
        self.filename = filename
        self.file_extension = os.path.splitext(filename)[1].lower()
        
        if isinstance(file_path_or_bytes, bytes):
            self.file_stream = io.BytesIO(file_path_or_bytes)
        else:
            self.file_stream = file_path_or_bytes

    def validate_file(self) -> None:
        """Validates file extension and size constraints."""
        if self.file_extension not in self.ALLOWED_EXTENSIONS:
            raise ValueError(f"Unsupported file format '{self.file_extension}'. Only PDF and DOCX are allowed.")
        
        self.file_stream.seek(0, os.SEEK_END)
        size = self.file_stream.tell()
        self.file_stream.seek(0)
        
        if size > self.MAX_FILE_SIZE_BYTES:
            raise ValueError(f"File size exceeds limit of {self.MAX_FILE_SIZE_MB}MB.")
        if size == 0:
            raise ValueError("Uploaded file is empty.")

    def _extract_from_pdf(self) -> str:
        text = ""
        try:
            reader = PyPDF2.PdfReader(self.file_stream)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted + "\n"
        except Exception as e:
            raise ValueError(f"Failed to parse PDF: {str(e)}")
        return text

    def _extract_from_docx(self) -> str:
        text = ""
        try:
            doc = docx.Document(self.file_stream)
            for para in doc.paragraphs:
                text += para.text + "\n"
        except Exception as e:
            raise ValueError(f"Failed to parse DOCX: {str(e)}")
        return text

    def parse(self) -> Dict[str, Any]:
        self.validate_file()
        
        if self.file_extension == ".pdf":
            raw_text = self._extract_from_pdf()
            file_type = "PDF"
        else:
            raw_text = self._extract_from_docx()
            file_type = "DOCX"
            
        return {
            "filename": self.filename,
            "file_type": file_type,
            "character_count": len(raw_text),
            "raw_text": raw_text
        }
