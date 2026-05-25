import fitz


def extract_layout_blocks(pdf_path: str):
    """
    Extrai blocos de layout do PDF usando PyMuPDF.

    Retorna uma lista de blocos com:
    - página
    - coordenadas
    - texto
    - tipo de bloco
    """

    document = fitz.open(pdf_path)

    layout_blocks = []

    for page_index, page in enumerate(document, start=1):

        blocks = page.get_text("blocks")

        for block_index, block in enumerate(blocks, start=1):

            x0, y0, x1, y1, text, block_no, block_type = block

            if not text.strip():
                continue

            layout_blocks.append(
                {
                    "pagina": page_index,
                    "bloco": block_index,
                    "x0": round(x0, 2),
                    "y0": round(y0, 2),
                    "x1": round(x1, 2),
                    "y1": round(y1, 2),
                    "largura": round(x1 - x0, 2),
                    "altura": round(y1 - y0, 2),
                    "texto": text.strip(),
                    "tipo_bloco_pdf": block_type
                }
            )

    document.close()

    return layout_blocks
