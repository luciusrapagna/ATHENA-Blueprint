import pandas as pd
from io import BytesIO


def create_excel_download(df: pd.DataFrame):
    """
    Cria arquivo Excel em memória para download no Streamlit.
    """

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="questoes")

    output.seek(0)

    return output
