import re


def is_support_text(text: str) -> bool:
    """
    Detecta textos de apoio compartilhados entre questões.
    """

    t = text.strip().lower()

    patterns = [
        r"texto\s+para\s+as?\s+questões?",
        r"texto\s+para\s+responder\s+às?\s+questões?",
        r"utilize\s+o\s+texto\s+a\s+seguir",
        r"leia\s+o\s+texto\s+a\s+seguir",
        r"considere\s+o\s+texto\s+a\s+seguir",
        r"com\s+base\s+no\s+texto\s+a\s+seguir",
        r"com\s+base\s+nas?\s+informações?\s+a\s+seguir",
        r"observe\s+o\s+texto\s+a\s+seguir",
        r"analise\s+o\s+texto\s+a\s+seguir",
        r"caso\s+clínico\s+para\s+as?\s+questões?",
        r"caso\s+clinico\s+para\s+as?\s+questões?",
        r"para\s+responder\s+às?\s+questões?\s+\d+",
        r"responda\s+às?\s+questões?\s+\d+",
    ]

    return any(re.search(pattern, t) for pattern in patterns)


def extract_support_question_range(text: str):
    """
    Tenta identificar a quais questões o texto de apoio se refere.

    Exemplos:
    - Texto para as questões 1 e 2
    - Para responder às questões 3 a 5
    """

    t = text.lower()

    match = re.search(r"questões?\s+(\d{1,3})\s+e\s+(\d{1,3})", t)
    if match:
        return list(range(int(match.group(1)), int(match.group(2)) + 1))

    match = re.search(r"questões?\s+(\d{1,3})\s+a\s+(\d{1,3})", t)
    if match:
        return list(range(int(match.group(1)), int(match.group(2)) + 1))

    match = re.search(r"questões?\s+(\d{1,3})", t)
    if match:
        return [int(match.group(1))]

    return []
