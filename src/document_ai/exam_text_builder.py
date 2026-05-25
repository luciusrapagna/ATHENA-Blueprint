import re


def is_page_number_block(block: dict) -> bool:
    """
    Detecta numeração de página por texto e posição.
    """

    text = block.get("texto", "").strip()
    y0 = block.get("y0", 0)
    y1 = block.get("y1", 0)

    if not re.fullmatch(r"\d{1,3}", text):
        return False

    # número isolado muito no topo ou muito no rodapé
    if y0 < 80 or y1 > 720:
        return True

    return False


def is_noise_block(block: dict) -> bool:
    """
    Identifica blocos que não devem entrar na reconstrução da prova.
    """

    text = block.get("texto", "").strip()
    t = text.lower()

    y0 = block.get("y0", 0)
    y1 = block.get("y1", 0)

    if not text:
        return True

    if is_page_number_block(block):
        return True

    # cabeçalho/rodapé por posição
    if y0 < 35:
        return True

    if y1 > 810:
        return True

    noise_patterns = [
        r"^medicina$",
        r"^área livre$",
        r"^area livre$",
        r"^rascunho$",
        r"^sinaes$",
        r"^ministério da educação$",
        r"^ministerio da educacao$",
        r"cartão-resposta",
        r"cartao-resposta",
        r"folha de respostas",
        r"caderno de respostas",
        r"boa sorte",
        r"não será permitido",
        r"nao sera permitido",
    ]

    return any(re.search(pattern, t) for pattern in noise_patterns)


def rebuild_exam_text(layout_blocks: list) -> str:
    """
    Reconstrói o texto útil da prova a partir dos blocos de layout,
    ignorando numeração de página, cabeçalhos, rodapés e ruídos.
    """

    useful_blocks = []

    for block in layout_blocks:

        if is_noise_block(block):
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
