def classify_theme(question_text: str, grande_area: str, subarea: str) -> str:
    text = question_text.lower()

    themes = {
        "Cardiologia": {
            "Insuficiência cardíaca": ["insuficiência cardíaca", "bnp", "fração de ejeção"],
            "Síndrome coronariana": ["infarto", "iam", "angina", "dor torácica"],
            "Arritmias": ["fibrilação atrial", "arritmia", "holter"],
            "Hipertensão arterial": ["hipertensão", "pressão arterial", "has"]
        },
        "Endocrinologia": {
            "Diabetes mellitus": ["diabetes", "insulina", "metformina", "glicemia", "hba1c"],
            "Tireoide": ["hipotireoidismo", "hipertireoidismo", "tireoide"],
            "Distúrbios metabólicos": ["cetoacidose", "hipoglicemia", "hiperglicemia"]
        },
        "Infectologia": {
            "Sepse": ["sepse", "choque séptico", "lactato"],
            "HIV/AIDS": ["hiv", "aids", "tarv", "cd4"],
            "Tuberculose": ["tuberculose", "ppd", "baciloscopia"]
        },
        "Trauma": {
            "ATLS": ["atls", "trauma", "politrauma"],
            "Choque hemorrágico": ["choque hemorrágico", "hemorragia"],
            "Trauma torácico": ["pneumotórax", "hemotórax", "drenagem torácica"]
        },
        "Abdome Agudo": {
            "Apendicite": ["apendicite"],
            "Obstrução intestinal": ["obstrução intestinal", "vômitos", "flatos"],
            "Colecistite": ["colecistite", "colangite"]
        },
        "Neonatologia": {
            "Recém-nascido": ["recém-nascido", "neonato", "apgar"],
            "Prematuridade": ["prematuro", "prematuridade"],
            "Triagem neonatal": ["teste do pezinho", "triagem neonatal"]
        },
        "Obstetrícia": {
            "Pré-natal": ["pré-natal", "gestante"],
            "Síndromes hipertensivas": ["pré-eclâmpsia", "eclâmpsia", "hellp"],
            "Parto": ["parto", "trabalho de parto", "cesariana"]
        },
        "APS": {
            "Atenção Primária": ["ubs", "esf", "atenção primária"],
            "Coordenação do cuidado": ["referência", "contrarreferência", "rede de atenção"],
            "Promoção da saúde": ["promoção", "educação em saúde"]
        },
        "Epidemiologia": {
            "Indicadores epidemiológicos": ["incidência", "prevalência", "mortalidade"],
            "Risco epidemiológico": ["risco relativo", "odds ratio"],
            "Vigilância": ["notificação", "sinan", "vigilância"]
        }
    }

    if subarea not in themes:
        return "Tema não identificado"

    scores = {}

    for theme, keywords in themes[subarea].items():
        scores[theme] = sum(1 for keyword in keywords if keyword in text)

    best_theme = max(scores, key=scores.get)

    if scores[best_theme] == 0:
        return "Tema não identificado"

    return best_theme
