import fitz  # PyMuPDF
from typing import List

def extract_text_from_pdf(pdf_path):
    """Extracts all text from a PDF file."""
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text("text") + "\n"
    return text

def chunk_text(text: str, chunk_words: int = 200) -> List[str]:
    """Splits text into chunks of N words."""
    words = text.split()
    return [" ".join(words[i:i + chunk_words]) for i in range(0, len(words), chunk_words)]
