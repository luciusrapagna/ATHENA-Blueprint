import re


def parse_enade_questions(text: str):
    text = re.sub(r'--- PÁGINA \d+ ---', '\n', text)
    text = re.sub(r'Área Livre|RASCUNHO', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'\*R\d+\*', '\n', text)
    text = re.sub(r'\n{2,}', '\n', text)

    pattern = r'(?=QUEST[ÃA]O(?:\s+DISCURSIVA)?\s*\d{1,3}\b)'

    blocks = re.split(pattern, text, flags=re.IGNORECASE)

    questions = []

    for block in blocks:
        block = block.strip()

        if re.search(r'QUEST[ÃA]O(?:\s+DISCURSIVA)?\s*\d{1,3}', block, flags=re.IGNORECASE):
            questions.append(block)

    return questions
