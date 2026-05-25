import re


def clean_text(text: str) -> str:
    """
    Remove cabeçalhos e marcas indesejadas.
    """

    text = re.sub(r'--- PÁGINA \d+ ---', '', text)

    return text


def extract_questions(text: str):

    text = clean_text(text)

    pattern = r'(?=\n\d{1,3}\.\s)'

    questions = re.split(pattern, text)

    questions = [
        q.strip()
        for q in questions
        if len(q.strip()) > 100
    ]

    return questions
