import re


def is_header_or_footer(text: str) -> bool:
    """
    Identifica textos que não fazem parte da questão.
    """

    t = text.strip().lower()

    ignored_patterns = [
        r"^\d+$",
        r"medicina$",
        r"enade",
        r"enamed",
        r"residência médica",
        r"fgv conhecimento",
        r"página\s+\d+",
        r"área livre",
        r"area livre",
        r"rascunho",
        r"questionário de percepção",
        r"questionario de percepcao",
        r"sinaes",
        r"ministério da educação",
        r"ministerio da educacao",
    ]

    for pattern in ignored_patterns:
        if re.search(pattern, t):
            return True

    return False


def rebuild_clean_text_from_layout(layout_blocks: list) -> str:
    """
    Reconstrói texto útil do PDF a partir dos blocos de layout,
    removendo cabeçalhos, rodapés, margens e elementos não avaliativos.
    """

    useful_blocks = []

    for block in layout_blocks:

        text = block.get("texto", "").strip()

        if not text:
            continue

        if is_header_or_footer(text):
            continue

        useful_blocks.append(block)

    useful_blocks = sorted(
        useful_blocks,
        key=lambda b: (b["pagina"], b["y0"], b["x0"])
    )

    clean_text = "\n".join(
        block["texto"].strip()
        for block in useful_blocks
    )

    clean_text = re.sub(r"\n{3,}", "\n\n", clean_text)

    return clean_text
