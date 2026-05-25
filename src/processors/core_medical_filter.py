import pandas as pd


CORE_MEDICAL_AREAS = [
    "Clínica Médica",
    "Cirurgia",
    "Pediatria",
    "Ginecologia e Obstetrícia",
    "Saúde Coletiva"
]


def keep_only_core_medical_areas(df: pd.DataFrame) -> pd.DataFrame:
    """
    Mantém apenas as 5 grandes áreas médicas principais.
    """

    if df.empty:
        return df

    filtered = df[
        df["grande_area"].isin(CORE_MEDICAL_AREAS)
    ].copy()

    return filtered
