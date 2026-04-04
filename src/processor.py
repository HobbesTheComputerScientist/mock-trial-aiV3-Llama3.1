import fitz  # PyMuPDF

def extract_text_from_pdf(file_obj) -> str:
    """Extract plain text from an uploaded PDF file object."""
    if file_obj is None:
        return ""
    try:
        doc = fitz.open(file_obj.name)
        text = "\n".join(page.get_text() for page in doc)
        doc.close()
        return text[:6000]  # cap to avoid exceeding context window
    except Exception as e:
        return f"[Error reading PDF: {e}]"
