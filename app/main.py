import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from src.parsers.parser_router import route_parser
from src.processors.question_structurer import structure_questions
from src.processors.excel_cleaner import clean_dataframe_for_excel
from src.processors.question_quality_filter import filter_complete_questions
from src.processors.core_medical_filter import keep_only_core_medical_areas
from src.document_ai.layout_extractor import extract_layout_blocks
from src.document_ai.exam_text_builder import rebuild_exam_text

from src.analytics.blueprint_analytics import (
    calculate_area_distribution,
    calculate_subarea_distribution,
    create_longitudinal_comparison,
    summarize_longitudinal_findings
)

from src.question_bank.bank_exporter import create_excel_download
from src.nlp.similarity_engine import calculate_question_similarity


st.set_page_config(
    page_title="ATHENA Blueprint",
    page_icon="🧠",
    layout="wide"
)

st.title("ATHENA Blueprint")
st.subheader("IA curricular médica — Blueprint semântico")

st.divider()

uploaded_files = st.file_uploader(
    "Faça upload de uma ou várias provas em PDF",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    raw_dir = Path("data/raw")
    processed_dir = Path("data/processed")
    figures_dir = Path("outputs/figures")

    raw_dir.mkdir(parents=True, exist_ok=True)
    processed_dir.mkdir(parents=True, exist_ok=True)
    figures_dir.mkdir(parents=True, exist_ok=True)

    all_core = []
    all_review = []

    for uploaded_file in uploaded_files:

        st.divider()
        st.subheader(f"Processando prova: {uploaded_file.name}")

        pdf_path = raw_dir / uploaded_file.name

        with open(pdf_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        layout_blocks = extract_layout_blocks(str(pdf_path))

        extracted_text = rebuild_exam_text(layout_blocks)

        output_txt_path = processed_dir / f"{pdf_path.stem}_texto_reconstruido.txt"

        with open(output_txt_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        exam_type, questions = route_parser(extracted_text)

        structured_questions = structure_questions(
            questions=questions,
            exam_type=exam_type
        )

        df_questions = pd.DataFrame(structured_questions)

        df_questions["arquivo_pdf"] = uploaded_file.name
        df_questions["nome_prova"] = pdf_path.stem

        df_questions = clean_dataframe_for_excel(df_questions)

        df_complete, df_review = filter_complete_questions(df_questions)

        df_core = keep_only_core_medical_areas(df_complete)

        all_core.append(df_core)
        all_review.append(df_review)

        st.info(f"Tipo detectado: {exam_type}")

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("Questões detectadas", len(df_questions))
        col2.metric("Questões completas", len(df_complete))
        col3.metric("5 grandes áreas", len(df_core))
        col4.metric("Para revisão", len(df_review))

        st.subheader("Distribuição nas 5 grandes áreas")

        df_distribution = calculate_area_distribution(df_core)

        st.dataframe(df_distribution)

        st.subheader("Distribuição por subárea")

        df_subarea_distribution = calculate_subarea_distribution(df_core)

        st.dataframe(df_subarea_distribution)

        if not df_distribution.empty:

            fig, ax = plt.subplots(figsize=(10, 6))

            ax.bar(
                df_distribution["grande_area"],
                df_distribution["percentual"]
            )

            ax.set_title(
                f"Distribuição percentual — 5 grandes áreas — {pdf_path.stem}"
            )

            ax.set_xlabel("Grande área")
            ax.set_ylabel("Percentual (%)")

            plt.xticks(rotation=45, ha="right")

            plt.tight_layout()

            figure_path = (
                figures_dir /
                f"{pdf_path.stem}_grafico_5_grandes_areas.png"
            )

            fig.savefig(
                figure_path,
                dpi=300,
                bbox_inches="tight"
            )

            st.pyplot(fig)

        st.subheader("Banco principal — 5 grandes áreas")

        st.dataframe(df_core)

        if not df_review.empty:

            st.warning(
                "Algumas questões foram separadas para revisão."
            )

            st.dataframe(df_review)

    if all_core:

        st.divider()

        st.header("Base consolidada — 5 grandes áreas")

        df_all_core = pd.concat(
            all_core,
            ignore_index=True
        )

        df_all_review = pd.concat(
            all_review,
            ignore_index=True
        )

        df_all_core = clean_dataframe_for_excel(df_all_core)

        df_all_review = clean_dataframe_for_excel(df_all_review)

        st.metric(
            "Total de questões nas 5 grandes áreas",
            len(df_all_core)
        )

        st.metric(
            "Total para revisão",
            len(df_all_review)
        )

        st.subheader("Distribuição consolidada")

        df_distribution_all = calculate_area_distribution(
            df_all_core
        )

        st.dataframe(df_distribution_all)

        st.subheader("Distribuição consolidada por subárea")

        df_subarea_all = calculate_subarea_distribution(
            df_all_core
        )

        st.dataframe(df_subarea_all)

        st.subheader("Comparação longitudinal")

        df_comparison = create_longitudinal_comparison(
            df_distribution_all
        )

        st.dataframe(df_comparison)

        st.subheader("Resumo longitudinal")

        df_summary = summarize_longitudinal_findings(
            df_distribution_all
        )

        st.dataframe(df_summary)

        st.subheader("Similaridade semântica entre questões")

        df_similarity = calculate_question_similarity(
            df_all_core,
            min_similarity=0.45
        )

        st.dataframe(df_similarity)

        similarity_excel = create_excel_download(df_similarity)

        st.download_button(
            label="Baixar matriz de similaridade entre questões",
            data=similarity_excel,
            file_name="similaridade_semantica_questoes.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

        st.subheader("Banco inteligente de questões por área")

        for area in sorted(
            df_all_core["grande_area"]
            .dropna()
            .unique()
        ):

            df_area = df_all_core[
                df_all_core["grande_area"] == area
            ].copy()

            excel_file = create_excel_download(df_area)

            st.download_button(
                label=f"Baixar banco de questões — {area}",
                data=excel_file,
                file_name=f"banco_questoes_{area}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.subheader(
            "Download da base consolidada completa"
        )

        consolidated_excel = create_excel_download(
            df_all_core
        )

        st.download_button(
            label="Baixar base consolidada — 5 grandes áreas",
            data=consolidated_excel,
            file_name="base_consolidada_5_grandes_areas.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
