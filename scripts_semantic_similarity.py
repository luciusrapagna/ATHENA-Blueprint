import os
import pandas as pd

from src.embeddings.embedding_engine import EmbeddingEngine


ARQUIVO_ENTRADA = "outputs/excel/base_consolidada_questoes_COMPLETAS.xlsx"
ARQUIVO_SAIDA = "outputs/semantic/similaridade_questoes.xlsx"


def escolher_coluna_texto(df):
    candidatas = ["questao", "texto_questao", "enunciado", "texto", "conteudo"]

    for coluna in candidatas:
        if coluna in df.columns:
            return coluna

    raise ValueError(
        f"Nenhuma coluna de texto encontrada. Colunas disponíveis: {list(df.columns)}"
    )


def garantir_questao_id(df):
    if "questao_id" not in df.columns:
        df["questao_id"] = ["Q" + str(i + 1) for i in range(len(df))]

    return df


def main():
    print("ATHENA | Similaridade semântica entre questões")

    if not os.path.exists(ARQUIVO_ENTRADA):
        raise FileNotFoundError(f"Arquivo não encontrado: {ARQUIVO_ENTRADA}")

    df = pd.read_excel(ARQUIVO_ENTRADA)
    print(f"Questões carregadas: {len(df)}")

    coluna_texto = escolher_coluna_texto(df)
    print(f"Coluna de texto usada: {coluna_texto}")

    df = garantir_questao_id(df)

    engine = EmbeddingEngine()

    resultado = engine.encontrar_questoes_semelhantes(
        dataframe=df,
        coluna_texto=coluna_texto,
        threshold=0.75
    )

    os.makedirs("outputs/semantic", exist_ok=True)

    resultado.to_excel(ARQUIVO_SAIDA, index=False)

    print(f"Arquivo gerado: {ARQUIVO_SAIDA}")
    print("Processo concluído com sucesso.")


if __name__ == "__main__":
    main()