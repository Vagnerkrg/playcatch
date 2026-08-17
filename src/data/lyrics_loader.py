from io import StringIO
from pathlib import Path
from urllib.parse import quote

import pandas as pd
import requests


DATASET_BASE_URL = (
    "https://huggingface.co/datasets/jamendolyrics/jamendolyrics/resolve/main/"
)

METADATA_URL = f"{DATASET_BASE_URL}JamendoLyrics.csv"

SOURCE_COLUMNS = [
    "Filepath",
    "Artist",
    "Title",
    "Language",
]

TARGET_COLUMNS = [
    "song_id",
    "title",
    "artist",
    "language",
    "lyrics",
]


def _load_metadata() -> pd.DataFrame:
    """Carrega os metadados textuais do dataset."""
    response = requests.get(METADATA_URL, timeout=30)
    response.raise_for_status()

    return pd.read_csv(StringIO(response.text))


def _load_lyrics(filepath: str) -> str:
    """Carrega a letra correspondente a um registro."""
    filename = Path(filepath).stem
    lyrics_url = f"{DATASET_BASE_URL}lyrics/{quote(filename)}.txt"

    response = requests.get(lyrics_url, timeout=30)
    response.raise_for_status()

    return response.text


def load_lyrics_dataset() -> pd.DataFrame:
    """Carrega metadados e letras sem baixar ou processar áudio."""
    metadata = _load_metadata()

    missing = [column for column in SOURCE_COLUMNS if column not in metadata.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    records = []

    for _, row in metadata.iterrows():
        records.append(
            {
                "song_id": Path(str(row["Filepath"])).stem,
                "title": row["Title"],
                "artist": row["Artist"],
                "language": row["Language"],
                "lyrics": _load_lyrics(str(row["Filepath"])),
            }
        )

    return pd.DataFrame(records, columns=TARGET_COLUMNS)
