from docx import Document

def extract_text_from_docx(docx_path):

    text = ""

    doc = Document(docx_path)

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text