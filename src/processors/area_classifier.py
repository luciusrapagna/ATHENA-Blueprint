def classify_large_area(question_text: str) -> str:
    """
    Classificador ampliado por palavras-chave para as 5 grandes áreas médicas.
    Futuramente poderá ser combinado com IA/NLP semântico.
    """

    text = question_text.lower()

    keyword_map = {

        "Clínica Médica": [
            "hipertensão", "hipertensao", "diabetes", "dislipidemia",
            "insuficiência cardíaca", "insuficiencia cardiaca", "iam",
            "infarto", "angina", "dor torácica", "dor toracica",
            "arritmia", "fibrilação atrial", "fibrilacao atrial",
            "avc", "acidente vascular cerebral", "trombose",
            "embolia pulmonar", "dispneia", "síncope", "sincope",
            "edema", "anemia", "leucemia", "linfoma", "plaquetopenia",
            "pneumonia", "asma", "dpoc", "tuberculose", "hiv",
            "aids", "hepatite", "cirrose", "ascite", "pancreatite",
            "gastrite", "úlcera", "ulcera", "doença renal",
            "doenca renal", "insuficiência renal", "insuficiencia renal",
            "glomerulonefrite", "lúpus", "lupus", "artrite reumatoide",
            "vasculite", "hipotireoidismo", "hipertireoidismo",
            "tireoide", "cetoacidose", "hipoglicemia", "hiperglicemia",
            "insulina", "metformina", "glicemia", "hemoglobina glicada",
            "creatinina", "ureia", "potássio", "potassio",
            "colesterol", "ldl", "hdl", "triglicerídeos",
            "triglicerideos", "sepse", "choque séptico", "choque septico",
            "delirium", "demência", "demencia", "convulsão", "convulsao",
            "cefaleia", "neuropatia", "parestesia", "parkinson",
            "depressão", "depressao", "ansiedade", "síndrome metabólica",
            "sindrome metabolica"
        ],

        "Cirurgia": [
            "abdome agudo", "apendicite", "colecistite", "colangite",
            "pancreatite aguda", "peritonite", "hérnia", "hernia",
            "hérnia inguinal", "hernia inguinal", "hérnia femoral",
            "hernia femoral", "obstrução intestinal", "obstrucao intestinal",
            "isquemia mesentérica", "isquemia mesenterica", "volvo",
            "intussuscepção", "intussuscepcao", "trauma", "politrauma",
            "atls", "ferimento por arma", "hemorragia", "choque hemorrágico",
            "choque hemorragico", "fratura", "luxação", "luxacao",
            "queimadura", "ferida", "sutura", "drenagem", "abscesso",
            "fasciíte", "fasciite", "toracocentese", "drenagem torácica",
            "drenagem toracica", "pneumotórax", "pneumotorax",
            "hemotórax", "hemotorax", "laparotomia", "laparoscopia",
            "pré-operatório", "pre-operatorio", "pós-operatório",
            "pos-operatorio", "anestesia", "pericardiocentese",
            "cricotireoidostomia", "toracotomia", "cirurgia", "cirúrgico",
            "cirurgico", "sala de emergência", "sala de emergencia",
            "lesão esplênica", "lesao esplenica", "abdome traumático",
            "abdome traumatico"
        ],

        "Pediatria": [
            "recém-nascido", "recem-nascido", "neonato", "neonatal",
            "lactente", "criança", "crianca", "escolar", "adolescente",
            "pediatria", "pediátrico", "pediatrico", "puericultura",
            "aleitamento materno", "amamentação", "amamentacao",
            "crescimento", "desenvolvimento infantil", "baixo peso ao nascer",
            "prematuro", "prematuridade", "apgar", "icterícia neonatal",
            "ictericia neonatal", "bronquiolite", "asma infantil",
            "diarreia aguda", "desidratação", "desidratacao",
            "soro de reidratação", "soro de reidratacao", "vacinação",
            "vacinacao", "calendário vacinal", "calendario vacinal",
            "exantema", "varicela", "sarampo", "coqueluche", "meningite",
            "sepse neonatal", "convulsão febril", "convulsao febril",
            "síndrome de down", "sindrome de down", "curvas de crescimento",
            "percentil", "imunização", "imunizacao", "desnutrição",
            "desnutricao", "obesidade infantil", "maus-tratos",
            "violência infantil", "violencia infantil", "teste do pezinho",
            "triagem neonatal"
        ],

        "Ginecologia e Obstetrícia": [
            "gestante", "gestação", "gestacao", "gravidez", "pré-natal",
            "pre-natal", "parto", "puerpério", "puerperio", "abortamento",
            "aborto", "eclâmpsia", "eclampsia", "pré-eclâmpsia",
            "pre-eclampsia", "síndrome hellp", "sindrome hellp",
            "diabetes gestacional", "hemorragia pós-parto",
            "hemorragia pos-parto", "placenta prévia", "placenta previa",
            "descolamento prematuro", "amniorrexe", "trabalho de parto",
            "cesariana", "colo uterino", "útero", "utero", "ovário",
            "ovario", "endométrio", "endometrio", "endometriose",
            "mioma", "miomatose", "sangramento uterino", "amenorreia",
            "dismenorreia", "dispareunia", "contracepção", "contracepcao",
            "anticoncepcional", "climatério", "climaterio", "menopausa",
            "corrimento vaginal", "vaginose", "candidíase vaginal",
            "candidiase vaginal", "doença inflamatória pélvica",
            "doenca inflamatoria pelvica", "dip", "hpv", "câncer de colo",
            "cancer de colo", "câncer de mama", "cancer de mama",
            "mamografia", "citopatológico", "citopatologico", "papanicolau",
            "sífilis na gestação", "sifilis na gestacao", "toxoplasmose na gestação",
            "toxoplasmose na gestacao", "rubéola na gestação", "rubeola na gestacao",
            "incompatibilidade rh", "sofrimento fetal", "restrição de crescimento fetal",
            "restricao de crescimento fetal"
        ],

        "Saúde Coletiva": [
            "sus", "sistema único de saúde", "sistema unico de saude",
            "atenção primária", "atencao primaria", "atenção básica",
            "atencao basica", "unidade básica de saúde",
            "unidade basica de saude", "ubs", "estratégia saúde da família",
            "estrategia saude da familia", "esf", "saúde da família",
            "saude da familia", "medicina de família", "medicina de familia",
            "território", "territorio", "adscrição", "adscricao",
            "vigilância em saúde", "vigilancia em saude",
            "vigilância epidemiológica", "vigilancia epidemiologica",
            "vigilância sanitária", "vigilancia sanitaria",
            "vigilância ambiental", "vigilancia ambiental",
            "saúde do trabalhador", "saude do trabalhador", "sinan",
            "notificação compulsória", "notificacao compulsoria",
            "epidemiologia", "incidência", "incidencia", "prevalência",
            "prevalencia", "mortalidade", "letalidade", "risco relativo",
            "odds ratio", "rastreamento", "prevenção", "prevencao",
            "promoção da saúde", "promocao da saude", "determinantes sociais",
            "equidade", "integralidade", "universalidade", "regionalização",
            "regionalizacao", "hierarquização", "hierarquizacao",
            "rede de atenção", "rede de atencao", "atenção secundária",
            "atencao secundaria", "atenção terciária", "atencao terciaria",
            "referência e contrarreferência", "referencia e contrarreferencia",
            "pse", "programa saúde na escola", "programa saude na escola",
            "política nacional", "politica nacional", "saúde coletiva",
            "saude coletiva", "vulnerabilidade", "linha de cuidado",
            "matriciamento", "apoio matricial", "promoção", "promocao",
            "educação em saúde", "educacao em saude"
        ],
    }

    scores = {}

    for area, keywords in keyword_map.items():
        scores[area] = sum(
            1 for keyword in keywords
            if keyword in text
        )

    best_area = max(scores, key=scores.get)

    if scores[best_area] == 0:
        return "Não classificada"

    return best_area
