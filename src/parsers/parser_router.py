from src.parsers.enade_parser import parse_enade_questions
from src.parsers.enamed_parser import parse_enamed_questions
from src.parsers.enare_parser import parse_enare_questions
from src.parsers.generic_parser import parse_generic_questions


def detect_exam_type(text: str) -> str:
    """
    Detecta automaticamente o tipo de prova.
    """

    upper_text = text.upper()

    if "EXAME NACIONAL DE RESIDÊNCIA" in upper_text or "RESIDÊNCIA MÉDICA" in upper_text:
        return "ENARE"

    if "ENAMED" in upper_text or "CADERNO 01" in upper_text:
        return "ENAMED"

    if "ENADE" in upper_text or "FORMAÇÃO GERAL" in upper_text:
        return "ENADE"

    return "GENÉRICO"


def route_parser(text: str):
    """
    Escolhe automaticamente o parser mais adequado.
    """

    exam_type = detect_exam_type(text)

    if exam_type == "ENARE":
        questions = parse_enare_questions(text)

    elif exam_type == "ENAMED":
        questions = parse_enamed_questions(text)

    elif exam_type == "ENADE":
        questions = parse_enade_questions(text)

    else:
        questions = parse_generic_questions(text)

    return exam_type, questions
