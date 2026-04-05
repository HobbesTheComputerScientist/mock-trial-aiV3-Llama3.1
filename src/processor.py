import fitz  # PyMuPDF

def extract_text_from_pdf(file_obj, max_chars=8000):
    """
    V3 Segmenter: Extracts text and prioritizes the core testimony.
    Capping at 8k ensures Llama-3.1-8B stays focused and fast.
    """
    if file_obj is None: 
        return ""
    
    try:
        with fitz.open(file_obj.name) as doc:
            # Efficiently join page text
            text = "\n".join(page.get_text() for page in doc)
        
        # ── SEGMENTER LOGIC ──
        if len(text) > max_chars:
            # Keep the start of the document where names/roles/dates usually are
            return text[:max_chars] + "\n\n... [SYSTEM NOTE: Text truncated to 8000 chars for focus] ..."
        return text
    except Exception as e:
        return f"⚠️ Error reading PDF: {e}"
