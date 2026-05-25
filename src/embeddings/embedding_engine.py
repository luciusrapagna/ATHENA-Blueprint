from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd


class EmbeddingEngine:

    def __init__(
        self,
        model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
    ):

        self.model = SentenceTransformer(model_name)

    def gerar_embeddings(self, textos):

        embeddings = self.model.encode(
            textos,
            convert_to_numpy=True,
            show_progress_bar=True
        )

        return embeddings

    def calcular_similaridade(self, embeddings):

        return cosine_similarity(embeddings)

    def encontrar_questoes_semelhantes(
        self,
        dataframe,
        coluna_texto="questao",
        threshold=0.80
    ):

        textos = dataframe[coluna_texto].fillna("").tolist()

        embeddings = self.gerar_embeddings(textos)

        similaridade = self.calcular_similaridade(embeddings)

        resultados = []

        for i in range(len(textos)):

            for j in range(i + 1, len(textos)):

                score = similaridade[i][j]

                if score >= threshold:

                    resultados.append({
                        "questao_1": dataframe.iloc[i]["questao_id"],
                        "questao_2": dataframe.iloc[j]["questao_id"],
                        "similaridade": round(float(score), 4)
                    })

        return pd.DataFrame(resultados)