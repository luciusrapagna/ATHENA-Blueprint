import os
import shutil
import subprocess
import pandas as pd
import streamlit as st
import plotly.express as px


st.set_page_config(
    page_title="ATHENA Blueprint",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 ATHENA Blueprint")
st.subheader("Medical Curriculum Intelligence Platform")


PASTA_PROVAS = "data/raw/provas_upload"
PASTA_PLANOS = "data/lesson_plans"

MATCH_PATH = "outputs/match/compatibilidade_curricular.xlsx"
TOP3_PATH = "outputs/match/compatibilidade_curricular_top3.xlsx"
GAPS_PATH = "outputs/analytics/lacunas_curriculares.xlsx"
HEATMAP_PATH = "outputs/figures/heatmap_curricular.png"
REPORT_MATCH = "outputs/word/relatorio_match_curricular.docx"
REPORT_GAPS = "outputs/word/relatorio_lacunas_curriculares.docx"


os.makedirs(PASTA_PROVAS, exist_ok=True)
os.makedirs(PASTA_PLANOS, exist_ok=True)


def carregar_excel(path):
    if os.path.exists(path):
        return pd.read_excel(path)
    return None


def salvar_uploads(uploaded_files, pasta_destino):
    salvos = []

    for uploaded_file in uploaded_files:
        caminho = os.path.join(pasta_destino, uploaded_file.name)

        with open(caminho, "wb") as f:
            f.write(uploaded_file.getbuffer())

        salvos.append(caminho)

    return salvos


aba0, aba1, aba2, aba3, aba4, aba5 = st.tabs([
    "Inserir Arquivos",
    "Visão Geral",
    "Match Curricular",
    "Top 3 Aulas",
    "Lacunas Curriculares",
    "Relatórios"
])


with aba0:
    st.header("Inserção de Dados para Análise")

    st.subheader("1. Inserir várias provas")

    provas = st.file_uploader(
        "Selecione uma ou mais provas",
        type=["pdf", "xlsx", "xls", "csv", "txt"],
        accept_multiple_files=True
    )

    if st.button("Salvar provas"):
        if provas:
            arquivos_salvos = salvar_uploads(provas, PASTA_PROVAS)
            st.success(f"{len(arquivos_salvos)} prova(s) salva(s) com sucesso.")
            st.write(arquivos_salvos)
        else:
            st.warning("Nenhuma prova foi selecionada.")

    st.divider()

    st.subheader("2. Inserir vários planos de aula")

    planos = st.file_uploader(
        "Selecione um ou mais planos de aula",
        type=["txt", "docx", "pdf"],
        accept_multiple_files=True
    )

    if st.button("Salvar planos de aula"):
        if planos:
            arquivos_salvos = salvar_uploads(planos, PASTA_PLANOS)
            st.success(f"{len(arquivos_salvos)} plano(s) salvo(s) com sucesso.")
            st.write(arquivos_salvos)
        else:
            st.warning("Nenhum plano de aula foi selecionado.")

    st.divider()

    st.subheader("3. Executar análises")

    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Rodar Match Curricular"):
            resultado = subprocess.run(
                ["python", "scripts_curricular_matching.py"],
                capture_output=True,
                text=True
            )
            st.code(resultado.stdout)
            if resultado.stderr:
                st.error(resultado.stderr)

    with col2:
        if st.button("Rodar Top 3 + Heatmap"):
            r1 = subprocess.run(
                ["python", "scripts_curricular_matching_top3.py"],
                capture_output=True,
                text=True
            )
            r2 = subprocess.run(
                ["python", "scripts_curricular_heatmap.py"],
                capture_output=True,
                text=True
            )
            st.code(r1.stdout)
            st.code(r2.stdout)
            if r1.stderr:
                st.error(r1.stderr)
            if r2.stderr:
                st.error(r2.stderr)

    with col3:
        if st.button("Rodar Lacunas + Relatórios"):
            comandos = [
                "scripts_detect_curricular_gaps.py",
                "scripts_generate_curricular_report.py",
                "scripts_generate_gap_report.py"
            ]

            for cmd in comandos:
                resultado = subprocess.run(
                    ["python", cmd],
                    capture_output=True,
                    text=True
                )
                st.code(resultado.stdout)
                if resultado.stderr:
                    st.error(resultado.stderr)



    st.divider()

    st.subheader("4. Limpar dados antigos")

    if st.button("Limpar uploads e resultados antigos"):
        import glob

        arquivos_limpar = []
        arquivos_limpar += glob.glob("outputs/match/*.xlsx")
        arquivos_limpar += glob.glob("outputs/analytics/*.xlsx")
        arquivos_limpar += glob.glob("outputs/figures/heatmap_curricular.png")
        arquivos_limpar += glob.glob("outputs/word/relatorio_match_curricular.docx")
        arquivos_limpar += glob.glob("outputs/word/relatorio_lacunas_curriculares.docx")
        arquivos_limpar += glob.glob("data/raw/provas_upload/*")
        arquivos_limpar += glob.glob("data/lesson_plans/*.txt")

        for arquivo in arquivos_limpar:
            try:
                os.remove(arquivo)
            except Exception:
                pass

        st.success("Dados antigos removidos. O ATHENA está pronto para nova análise.")

with aba1:
    st.header("Visão Geral do ATHENA")

    df_match = carregar_excel(MATCH_PATH)
    df_top3 = carregar_excel(TOP3_PATH)
    df_gaps = carregar_excel(GAPS_PATH)

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Questões analisadas",
            df_match["questao"].nunique() if df_match is not None else "Não disponível"
        )

    with col2:
        st.metric(
            "Associações Top 3",
            len(df_top3) if df_top3 is not None else "Não disponível"
        )

    with col3:
        st.metric(
            "Aulas avaliadas",
            len(df_gaps) if df_gaps is not None else "Não disponível"
        )

    st.divider()

    if os.path.exists(HEATMAP_PATH):
        st.image(HEATMAP_PATH, caption="Heatmap de Compatibilidade Curricular")
    else:
        st.warning("Heatmap ainda não encontrado.")


with aba2:
    st.header("Match Curricular Principal")

    df_match = carregar_excel(MATCH_PATH)

    if df_match is not None:
        st.dataframe(df_match, use_container_width=True)

        fig = px.histogram(
            df_match,
            x="compatibilidade_percentual",
            nbins=20,
            title="Distribuição da Compatibilidade Curricular"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Arquivo de match curricular não encontrado.")


with aba3:
    st.header("Top 3 Aulas Compatíveis por Questão")

    df_top3 = carregar_excel(TOP3_PATH)

    if df_top3 is not None:
        st.dataframe(df_top3, use_container_width=True)

        resumo = (
            df_top3.groupby("aula_compativel")
            .agg(media_compatibilidade=("compatibilidade_percentual", "mean"))
            .reset_index()
        )

        fig = px.bar(
            resumo,
            x="aula_compativel",
            y="media_compatibilidade",
            title="Média de Compatibilidade por Aula"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Arquivo Top 3 não encontrado.")


with aba4:
    st.header("Detecção de Lacunas Curriculares")

    df_gaps = carregar_excel(GAPS_PATH)

    if df_gaps is not None:
        st.dataframe(df_gaps, use_container_width=True)

        fig = px.pie(
            df_gaps,
            names="status_curricular",
            title="Distribuição dos Status Curriculares"
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning("Arquivo de lacunas curriculares não encontrado.")


with aba5:
    st.header("Relatórios Institucionais")

    if os.path.exists(REPORT_MATCH):
        with open(REPORT_MATCH, "rb") as file:
            st.download_button(
                label="Baixar Relatório de Match Curricular",
                data=file,
                file_name="relatorio_match_curricular.docx"
            )

    if os.path.exists(REPORT_GAPS):
        with open(REPORT_GAPS, "rb") as file:
            st.download_button(
                label="Baixar Relatório de Lacunas Curriculares",
                data=file,
                file_name="relatorio_lacunas_curriculares.docx"
            )

