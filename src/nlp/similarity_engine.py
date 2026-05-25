import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calculate_question_similarity(df: pd.DataFrame, min_similarity: float = 0.45) -> pd.DataFrame:
    """
    Calcula similaridade textual entre questões usando TF-IDF + cosseno.
    Esta é uma versão inicial leve, sem embeddings pesados.
    """

    if df.empty or "texto_completo" not in df.columns:
        return pd.DataFrame(
            columns=[
                "questao_1",
                "prova_1",
                "area_1",
                "tema_1",
                "questao_2",
                "prova_2",
                "area_2",
                "tema_2",
                "similaridade"
            ]
        )

    df_work = df.reset_index(drop=True).copy()

    texts = df_work["texto_completo"].fillna("").astype(str).tolist()

    if len(texts) < 2:
        return pd.DataFrame()

    vectorizer = TfidfVectorizer(
        lowercase=True,
        stop_words=None,
        ngram_range=(1, 2),
        max_features=5000
    )

    matrix = vectorizer.fit_transform(texts)

    similarity_matrix = cosine_similarity(matrix)

    results = []

    for i in range(len(df_work)):
        for j in range(i + 1, len(df_work)):

            score = float(similarity_matrix[i, j])

            if score >= min_similarity:

                results.append(
                    {
                        "questao_1": df_work.loc[i, "numero"],
                        "prova_1": df_work.loc[i, "nome_prova"],
                        "area_1": df_work.loc[i, "grande_area"],
                        "tema_1": df_work.loc[i].get("tema", ""),
                        "questao_2": df_work.loc[j, "numero"],
                        "prova_2": df_work.loc[j, "nome_prova"],
                        "area_2": df_work.loc[j, "grande_area"],
                        "tema_2": df_work.loc[j].get("tema", ""),
                        "similaridade": round(score * 100, 2)
                    }
                )

    result_df = pd.DataFrame(results)

    if result_df.empty:
        return result_df

    return result_df.sort_values(
        by="similaridade",
        ascending=False
    )
