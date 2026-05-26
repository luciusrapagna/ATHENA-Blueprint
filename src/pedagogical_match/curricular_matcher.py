import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from src.embeddings.embedding_engine import EmbeddingEngine


class CurricularMatcher:
    def __init__(self, model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"):
        self.embedding_engine = EmbeddingEngine(model_name=model_name)

    def match_questions_to_lessons(
        self,
        questions_df: pd.DataFrame,
        lessons_df: pd.DataFrame,
        question_text_col: str = "enunciado"
    ) -> pd.DataFrame:

        if question_text_col not in questions_df.columns:
            raise ValueError(f"Coluna textual '{question_text_col}' não encontrada nas questões.")

        if "aula" not in lessons_df.columns or "conteudo" not in lessons_df.columns:
            raise ValueError("O dataframe de aulas precisa conter as colunas: 'aula' e 'conteudo'.")

        question_texts = questions_df[question_text_col].fillna("").astype(str).tolist()
        lesson_texts = lessons_df["conteudo"].fillna("").astype(str).tolist()

        question_embeddings = self.embedding_engine.gerar_embeddings(question_texts)
        lesson_embeddings = self.embedding_engine.gerar_embeddings(lesson_texts)

        similarity_matrix = cosine_similarity(question_embeddings, lesson_embeddings)

        results = []

        for i, question in enumerate(question_texts):
            best_lesson_index = similarity_matrix[i].argmax()
            best_score = similarity_matrix[i][best_lesson_index]

            row = {
                "questao": i + 1,
                "enunciado": question,
                "aula_mais_compativel": lessons_df.iloc[best_lesson_index]["aula"],
                "conteudo_da_aula": lessons_df.iloc[best_lesson_index]["conteudo"],
                "compatibilidade_percentual": round(best_score * 100, 2),
                "recomendacao_pedagogica": self._generate_recommendation(best_score)
            }

            for col in ["Grande Área", "grande_area", "Tema", "tema", "cluster", "cluster_semantico"]:
                if col in questions_df.columns:
                    row[col] = questions_df.iloc[i][col]

            results.append(row)

        return pd.DataFrame(results)

    def _generate_recommendation(self, score: float) -> str:
        if score >= 0.70:
            return "Alta compatibilidade curricular. Questão fortemente associada ao plano de aula."
        elif score >= 0.50:
            return "Compatibilidade moderada. Questão pode ser utilizada como apoio ou revisão."
        elif score >= 0.35:
            return "Compatibilidade baixa. Recomenda-se revisão pedagógica antes da associação."
        else:
            return "Baixa aderência curricular. Questão pouco compatível com as aulas cadastradas."

    def match_questions_to_top_lessons(
        self,
        questions_df: pd.DataFrame,
        lessons_df: pd.DataFrame,
        question_text_col: str = "enunciado",
        top_n: int = 3
    ) -> pd.DataFrame:

        if question_text_col not in questions_df.columns:
            raise ValueError(f"Coluna textual '{question_text_col}' não encontrada nas questões.")

        if "aula" not in lessons_df.columns or "conteudo" not in lessons_df.columns:
            raise ValueError("O dataframe de aulas precisa conter as colunas: 'aula' e 'conteudo'.")

        question_texts = questions_df[question_text_col].fillna("").astype(str).tolist()
        lesson_texts = lessons_df["conteudo"].fillna("").astype(str).tolist()

        question_embeddings = self.embedding_engine.gerar_embeddings(question_texts)
        lesson_embeddings = self.embedding_engine.gerar_embeddings(lesson_texts)

        similarity_matrix = cosine_similarity(question_embeddings, lesson_embeddings)

        results = []

        for i, question in enumerate(question_texts):
            ranked_indexes = similarity_matrix[i].argsort()[::-1][:top_n]

            for rank, lesson_index in enumerate(ranked_indexes, start=1):
                score = similarity_matrix[i][lesson_index]

                row = {
                    "questao": i + 1,
                    "ranking_aula": rank,
                    "enunciado": question,
                    "aula_compativel": lessons_df.iloc[lesson_index]["aula"],
                    "conteudo_da_aula": lessons_df.iloc[lesson_index]["conteudo"],
                    "compatibilidade_percentual": round(score * 100, 2),
                    "recomendacao_pedagogica": self._generate_recommendation(score)
                }

                for col in ["Grande Área", "grande_area", "Tema", "tema", "cluster", "cluster_semantico"]:
                    if col in questions_df.columns:
                        row[col] = questions_df.iloc[i][col]

                results.append(row)

        return pd.DataFrame(results)
