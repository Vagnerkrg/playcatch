import re

import pandas as pd


def clean_lyrics(text: str) -> str:
    """Limpa e normaliza uma letra sem alterar seu conteúdo semântico."""
    if not isinstance(text, str):
        return ""

    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


def clean_lyrics_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Valida e normaliza o dataframe de letras."""
    result = df.copy()

    required_columns = [
        "song_id",
        "title",
        "artist",
        "language",
        "lyrics",
    ]

    missing = [column for column in required_columns if column not in result]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    result["lyrics"] = result["lyrics"].fillna("").map(clean_lyrics)

    result = result[result["lyrics"].str.len() > 0].copy()

    return result.reset_index(drop=True)
