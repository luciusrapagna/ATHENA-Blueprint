import re


def parse_enare_questions(text: str):
    text = re.sub(r'--- PÁGINA \d+ ---', '\n', text)
    text = re.sub(r'Residência Médica FGV Conhecimento', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'Acesso Direto.*?Página\s+\d+', '\n', text, flags=re.IGNORECASE)
    text = re.sub(r'\n{2,}', '\n', text)

    pattern = r'(?=\n\s*\d{1,3}\s*\n)'

    blocks = re.split(pattern, text)

    questions = []

    for block in blocks:
        block = block.strip()

        if re.match(r'^\d{1,3}\s+', block):
            questions.append(block)

    return questions
