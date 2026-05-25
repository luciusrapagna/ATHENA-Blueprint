def classify_subarea(question_text: str, grande_area: str) -> str:
    """
    Classifica subáreas médicas por NLP baseado em palavras-chave.
    """

    text = question_text.lower()

    subareas = {

        "Clínica Médica": {

            "Cardiologia": [
                "infarto", "iam", "angina", "ecg",
                "arritmia", "fibrilação atrial",
                "insuficiência cardíaca", "hipertensão"
            ],

            "Endocrinologia": [
                "diabetes", "insulina", "hipotireoidismo",
                "hipertireoidismo", "metformina",
                "glicemia", "cetoacidose"
            ],

            "Pneumologia": [
                "asma", "dpoc", "pneumonia",
                "tuberculose", "dispneia"
            ],

            "Nefrologia": [
                "creatinina", "hemodiálise",
                "dialise", "glomerulonefrite",
                "doença renal"
            ],

            "Infectologia": [
                "sepse", "choque séptico",
                "antibiótico", "antibiotico",
                "hiv", "aids", "hepatite"
            ]
        },

        "Cirurgia": {

            "Trauma": [
                "politrauma", "atls", "hemorragia",
                "fratura", "choque hemorrágico"
            ],

            "Abdome Agudo": [
                "abdome agudo", "apendicite",
                "colecistite", "peritonite"
            ],

            "Cirurgia Vascular": [
                "isquemia", "aneurisma",
                "trombose", "embolia"
            ]
        },

        "Pediatria": {

            "Neonatologia": [
                "apgar", "prematuro",
                "recém-nascido", "neonato"
            ],

            "Pediatria Ambulatorial": [
                "vacinação", "crescimento",
                "desenvolvimento", "puericultura"
            ]
        },

        "Ginecologia e Obstetrícia": {

            "Obstetrícia": [
                "gestante", "pré-natal",
                "parto", "eclâmpsia"
            ],

            "Ginecologia": [
                "endometriose", "mioma",
                "colo uterino", "menopausa"
            ]
        },

        "Saúde Coletiva": {

            "Epidemiologia": [
                "incidência", "prevalência",
                "risco relativo", "odds ratio"
            ],

            "APS": [
                "ubs", "esf", "atenção primária",
                "saúde da família"
            ],

            "Políticas Públicas": [
                "sus", "integralidade",
                "equidade", "universalidade"
            ]
        }
    }

    if grande_area not in subareas:
        return "Não classificada"

    scores = {}

    for subarea, keywords in subareas[grande_area].items():

        scores[subarea] = sum(
            1 for keyword in keywords
            if keyword.lower() in text
        )

    best_subarea = max(scores, key=scores.get)

    if scores[best_subarea] == 0:
        return "Subárea não identificada"

    return best_subarea
