import re


def parse_alternatives(question_text: str):
    """
    Separa alternativas A, B, C, D e E quando existirem.

    Reconhece formatos:
    A texto
    B texto
    (A) texto
    (B) texto
    A) texto
    B) texto
    """

    pattern = r'(?=\n?\s*\(?[A-E]\)?[\.\)]?\s+)'

    parts = re.split(pattern, question_text)

    enunciado = parts[0].strip() if parts else question_text.strip()

    alternatives = {
        "alternativa_a": None,
        "alternativa_b": None,
        "alternativa_c": None,
        "alternativa_d": None,
        "alternativa_e": None,
    }

    for part in parts[1:]:

        part = part.strip()

        match = re.match(r'^\(?([A-E])\)?[\.\)]?\s+(.*)', part, flags=re.DOTALL)

        if match:
            letter = match.group(1).lower()
            content = match.group(2).strip()

            alternatives[f"alternativa_{letter}"] = content

    return enunciado, alternatives


def evaluate_reading_status(alternatives: dict):
    """
    Avalia se a questão parece ter sido lida corretamente.
    """

    filled = sum(
        1 for value in alternatives.values()
        if value is not None and len(value.strip()) > 0
    )

    if filled == 0:
        return "Sem alternativas"

    if filled < 4:
        return "Questão possivelmente partida"

    return "OK"
