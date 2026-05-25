def classify_cognitive_level(question_text: str) -> str:
    text = question_text.lower()

    if any(term in text for term in [
        "qual é a conduta", "conduta adequada", "tratamento",
        "manejo", "intervenção", "deve-se proceder"
    ]):
        return "Aplicação clínica"

    if any(term in text for term in [
        "principal hipótese", "diagnóstico", "quadro clínico",
        "é correto afirmar", "considerando o caso"
    ]):
        return "Raciocínio diagnóstico"

    if any(term in text for term in [
        "interprete", "exames", "laboratoriais", "ecg",
        "tomografia", "ressonância", "radiografia"
    ]):
        return "Interpretação de dados"

    if any(term in text for term in [
        "conceito", "define", "caracteriza", "assinale a opção correta"
    ]):
        return "Conhecimento conceitual"

    return "Nível cognitivo não identificado"
