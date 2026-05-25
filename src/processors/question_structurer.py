import re

from src.processors.area_classifier import classify_large_area
from src.processors.alternative_parser import (
    parse_alternatives,
    evaluate_reading_status
)
from src.nlp.subarea_classifier import classify_subarea
from src.nlp.theme_classifier import classify_theme
from src.nlp.competency_classifier import classify_competency
from src.nlp.cognitive_level_classifier import classify_cognitive_level


def extract_question_number(question_text: str):

    match = re.search(
        r'QUEST[ÃA]O\s*(?:DISCURSIVA\s*)?(\d{1,3})',
        question_text,
        flags=re.IGNORECASE
    )

    if match:
        return int(match.group(1))

    match = re.match(r'^(\d{1,3})\s+', question_text.strip())

    if match:
        return int(match.group(1))

    return None


def structure_questions(questions: list, exam_type: str):

    structured = []

    for question in questions:

        enunciado, alternatives = parse_alternatives(question)
        status_leitura = evaluate_reading_status(alternatives)

        grande_area = classify_large_area(question)
        subarea = classify_subarea(question, grande_area)
        tema = classify_theme(question, grande_area, subarea)
        competencia = classify_competency(question)
        nivel_cognitivo = classify_cognitive_level(question)

        item = {
            "numero": extract_question_number(question),
            "tipo_prova": exam_type,
            "grande_area": grande_area,
            "subarea": subarea,
            "tema": tema,
            "competencia": competencia,
            "nivel_cognitivo": nivel_cognitivo,
            "status_leitura": status_leitura,
            "enunciado": enunciado,
            "alternativa_a": alternatives.get("alternativa_a"),
            "alternativa_b": alternatives.get("alternativa_b"),
            "alternativa_c": alternatives.get("alternativa_c"),
            "alternativa_d": alternatives.get("alternativa_d"),
            "alternativa_e": alternatives.get("alternativa_e"),
            "texto_completo": question
        }

        structured.append(item)

    return structured
