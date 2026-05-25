import re
from openpyxl.cell.cell import ILLEGAL_CHARACTERS_RE


def clean_for_excel(value):
    """
    Remove caracteres ilegais que impedem o salvamento no Excel.
    """

    if isinstance(value, str):
        value = ILLEGAL_CHARACTERS_RE.sub("", value)
        value = re.sub(r"[\x00-\x08\x0B-\x0C\x0E-\x1F]", "", value)
        return value

    return value


def clean_dataframe_for_excel(df):
    """
    Aplica limpeza em todas as células textuais do DataFrame.
    """

    return df.map(clean_for_excel)
