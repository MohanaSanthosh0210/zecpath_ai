import os
from docx import Document


def extract_text_from_docx(docx_path: str) -> str:

    text = ""

    doc = Document(docx_path)

    for para in doc.paragraphs:

        if para.text:
            text += para.text + "\n"

    return text


class DocumentReader:
    """
    Universal resume reader for ATS pipelines.
    Supports PDF and DOCX extraction through a stable common interface.
    """

    def extract_text(self, resume_path: str) -> str:
        ext = os.path.splitext(resume_path)[1].lower()

        if ext == ".docx":
            return extract_text_from_docx(resume_path)

        if ext == ".pdf":
            from .pdf_reader import extract_text_from_pdf

            return extract_text_from_pdf(resume_path)

        raise ValueError(
            f"Unsupported document format: {ext}. Supported formats are .pdf and .docx."
        )