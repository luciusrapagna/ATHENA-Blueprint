def classify_competency(question_text: str) -> str:
    text = question_text.lower()

    competency_map = {
        "Diagnóstico clínico": [
            "diagnóstico", "hipótese diagnóstica", "quadro clínico",
            "principal hipótese", "diagnostico"
        ],
        "Conduta terapêutica": [
            "conduta", "tratamento", "terapia", "prescrição",
            "manejo", "intervenção"
        ],
        "Interpretação de exames": [
            "exames laboratoriais", "ecocardiograma", "tomografia",
            "ressonância", "hemograma", "eletrocardiograma", "ecg"
        ],
        "Urgência e emergência": [
            "emergência", "urgência", "choque", "trauma",
            "pronto-socorro", "upa", "samu"
        ],
        "Prevenção e promoção da saúde": [
            "prevenção", "promoção", "rastreamento", "vacinação",
            "educação em saúde"
        ],
        "Atenção Primária e SUS": [
            "sus", "ubs", "esf", "atenção primária",
            "atenção básica", "saúde da família"
        ]
    }

    scores = {}

    for competency, keywords in competency_map.items():
        scores[competency] = sum(1 for keyword in keywords if keyword in text)

    best = max(scores, key=scores.get)

    if scores[best] == 0:
        return "Competência não identificada"

    return best
