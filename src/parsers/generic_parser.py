import re


def parse_generic_questions(text: str):
    """
    Parser genérico para provas médicas com padrões variados.
    Usado como fallback quando o tipo da prova não é identificado.
    """

    text = re.sub(r'--- PÁGINA \d+ ---', '\n', text)
    text = re.sub(r'ÁREA LIVRE|Área Livre|RASCUNHO', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'\n{3,}', '\n\n', text)

    pattern = r'(?=(?:QUEST[ÃA]O\s+\d{1,3}|\n\s*\d{1,3}\s*\n))'

    blocks = re.split(pattern, text, flags=re.IGNORECASE)

    questions = []

    for block in blocks:
        block = block.strip()

        if len(block) < 120:
            continue

        if (
            re.search(r'QUEST[ÃA]O\s+\d{1,3}', block, flags=re.IGNORECASE)
            or re.match(r'^\d{1,3}\s+', block)
        ):
            questions.append(block)

    return questions
