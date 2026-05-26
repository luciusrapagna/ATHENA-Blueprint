import os
import pandas as pd

from src.pedagogical_match.lesson_plan_reader import LessonPlanReader
from src.pedagogical_match.curricular_matcher import CurricularMatcher


QUESTIONS_PATH = "outputs/semantic/clusters_semanticos.xlsx"
OUTPUT_PATH = "outputs/match/compatibilidade_curricular.xlsx"


def detectar_coluna_textual(df):
    possiveis = ["enunciado", "questao", "texto", "pergunta", "Questão", "Enunciado"]

    for col in possiveis:
        if col in df.columns:
            return col

    raise ValueError("Nenhuma coluna textual compatível foi encontrada.")


def main():
    print("=" * 70)
    print("ATHENA Blueprint — MATCH PEDAGÓGICO INTELIGENTE")
    print("=" * 70)

    print("\n[1] LENDO BANCO DE QUESTÕES...")
    questions_df = pd.read_excel(QUESTIONS_PATH)

    print(f"Total de questões carregadas: {len(questions_df)}")

    question_text_col = detectar_coluna_textual(questions_df)
    print(f"Coluna textual detectada: {question_text_col}")

    print("\n[2] LENDO PLANOS DE AULA...")
    reader = LessonPlanReader()
    lessons_df = reader.carregar_planos()

    print(f"Total de aulas detectadas: {len(lessons_df)}")

    lessons_df = lessons_df.rename(columns={"texto_aula": "conteudo"})

    print("\n[3] CALCULANDO SIMILARIDADE SEMÂNTICA...")
    matcher = CurricularMatcher()

    result_df = matcher.match_questions_to_lessons(
        questions_df=questions_df,
        lessons_df=lessons_df,
        question_text_col=question_text_col
    )

    print("\n[4] GERANDO ARQUIVO FINAL...")
    os.makedirs("outputs/match", exist_ok=True)

    result_df.to_excel(OUTPUT_PATH, index=False)

    print("\n" + "=" * 70)
    print("MATCH PEDAGÓGICO FINALIZADO COM SUCESSO")
    print("=" * 70)
    print(f"\nArquivo gerado: {OUTPUT_PATH}")
    print("\nPRÉVIA DOS RESULTADOS:\n")

    print(result_df[["questao", "aula_mais_compativel", "compatibilidade_percentual"]].head())


if __name__ == "__main__":
    main()
