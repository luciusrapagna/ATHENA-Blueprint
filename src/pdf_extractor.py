import fitz  # PyMuPDF


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extrai o texto completo de um arquivo PDF.

    Parâmetro:
        pdf_path: caminho do arquivo PDF

    Retorno:
        texto extraído do PDF
    """
    text = ""

    with fitz.open(pdf_path) as document:
        for page_number, page in enumerate(document, start=1):
            page_text = page.get_text()
            text += f"\n\n--- PÁGINA {page_number} ---\n"
            text += page_text

    return text