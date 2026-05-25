import pandas as pd


def calculate_area_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula número e percentual de questões por grande área e por prova.
    """

    if df.empty:
        return pd.DataFrame(
            columns=[
                "nome_prova",
                "grande_area",
                "n_questoes",
                "total_questoes",
                "percentual"
            ]
        )

    grouped = (
        df.groupby(["nome_prova", "grande_area"])
        .size()
        .reset_index(name="n_questoes")
    )

    totals = (
        df.groupby("nome_prova")
        .size()
        .reset_index(name="total_questoes")
    )

    result = grouped.merge(totals, on="nome_prova", how="left")

    result["percentual"] = (
        result["n_questoes"] / result["total_questoes"] * 100
    ).round(2)

    return result.sort_values(
        by=["nome_prova", "percentual"],
        ascending=[True, False]
    )


def calculate_subarea_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """
    Calcula distribuição por subárea dentro de cada grande área.
    """

    if df.empty or "subarea" not in df.columns:
        return pd.DataFrame(
            columns=[
                "nome_prova",
                "grande_area",
                "subarea",
                "n_questoes",
                "total_area",
                "percentual_na_area"
            ]
        )

    grouped = (
        df.groupby(["nome_prova", "grande_area", "subarea"])
        .size()
        .reset_index(name="n_questoes")
    )

    totals = (
        df.groupby(["nome_prova", "grande_area"])
        .size()
        .reset_index(name="total_area")
    )

    result = grouped.merge(
        totals,
        on=["nome_prova", "grande_area"],
        how="left"
    )

    result["percentual_na_area"] = (
        result["n_questoes"] / result["total_area"] * 100
    ).round(2)

    return result.sort_values(
        by=["nome_prova", "grande_area", "percentual_na_area"],
        ascending=[True, True, False]
    )


def create_longitudinal_comparison(df_distribution: pd.DataFrame) -> pd.DataFrame:
    """
    Cria matriz comparativa entre provas.
    """

    if df_distribution.empty:
        return pd.DataFrame()

    comparison = df_distribution.pivot_table(
        index="nome_prova",
        columns="grande_area",
        values="percentual",
        fill_value=0
    ).reset_index()

    return comparison


def summarize_longitudinal_findings(df_distribution: pd.DataFrame) -> pd.DataFrame:
    """
    Gera resumo indicando, para cada área, qual prova teve maior percentual.
    """

    if df_distribution.empty:
        return pd.DataFrame(
            columns=[
                "grande_area",
                "prova_com_maior_percentual",
                "maior_percentual"
            ]
        )

    idx = df_distribution.groupby("grande_area")["percentual"].idxmax()

    summary = df_distribution.loc[
        idx,
        ["grande_area", "nome_prova", "percentual"]
    ].copy()

    summary = summary.rename(
        columns={
            "nome_prova": "prova_com_maior_percentual",
            "percentual": "maior_percentual"
        }
    )

    return summary.sort_values(by="grande_area")
