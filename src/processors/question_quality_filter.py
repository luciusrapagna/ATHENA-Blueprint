def filter_complete_questions(df):
    """
    Mantém no banco principal apenas questões estruturalmente completas.
    """

    df_complete = df[df["status_leitura"] == "OK"].copy()

    df_review = df[df["status_leitura"] != "OK"].copy()

    return df_complete, df_review
