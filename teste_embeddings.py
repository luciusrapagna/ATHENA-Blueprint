import pandas as pd

from src.embeddings.embedding_engine import EmbeddingEngine


dados = pd.DataFrame({

    "questao_id": [
        "Q1",
        "Q2",
        "Q3"
    ],

    "questao": [

        "Paciente com infarto agudo do miocárdio apresentando dor torácica.",

        "Homem com IAM apresenta dor no peito e alterações eletrocardiográficas.",

        "Criança com bronquiolite viral apresenta desconforto respiratório."
    ]
})


engine = EmbeddingEngine()

resultado = engine.encontrar_questoes_semelhantes(
    dados,
    threshold=0.50
)

print(resultado)