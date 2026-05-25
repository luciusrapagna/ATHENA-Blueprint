import os
import pandas as pd

from src.embeddings.embedding_engine import EmbeddingEngine
from src.nlp.semantic_cluster_engine import SemanticClusterEngine


ARQUIVO = "outputs/excel/base_consolidada_questoes_COMPLETAS.xlsx"


def escolher_coluna_texto(df):

    candidatas = [
        "questao",
        "texto_questao",
        "enunciado",
        "texto",
        "conteudo"
    ]

    for coluna in candidatas:

        if coluna in df.columns:
            return coluna

    raise ValueError(
        f"Nenhuma coluna textual encontrada. Colunas: {list(df.columns)}"
    )


def main():

    print("ATHENA | Semantic Clustering")

    if not os.path.exists(ARQUIVO):
        raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO}")

    df = pd.read_excel(ARQUIVO)

    print(f"Questões carregadas: {len(df)}")

    coluna_texto = escolher_coluna_texto(df)

    print(f"Coluna usada: {coluna_texto}")

    textos = df[coluna_texto].fillna("").tolist()

    embedding_engine = EmbeddingEngine()

    embeddings = embedding_engine.gerar_embeddings(textos)

    cluster_engine = SemanticClusterEngine(
        n_clusters=5
    )

    resultado = cluster_engine.criar_dataframe_cluster(
        dataframe=df,
        embeddings=embeddings
    )

    os.makedirs("outputs/semantic", exist_ok=True)

    arquivo_saida = "outputs/semantic/clusters_semanticos.xlsx"

    resultado.to_excel(
        arquivo_saida,
        index=False
    )

    print(f"Arquivo salvo: {arquivo_saida}")

    print("Clusterização concluída com sucesso.")


if __name__ == "__main__":
    main()