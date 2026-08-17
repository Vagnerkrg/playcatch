from pathlib import Path

import pandas as pd


DEFAULT_DATASET_PATH = Path("data/processed/lyrics_sentiment.csv")

REQUIRED_COLUMNS = [
    "song_id",
    "title",
    "artist",
    "language",
    "lyrics",
    "emotion",
    "score",
]

VALID_EMOTIONS = {
    "anger",
    "fear",
    "joy",
    "sadness",
}


class SentimentDataLoader:
    """Carrega e valida os dados de sentimento da Milestone 1."""

    def __init__(self, dataset_path: Path = DEFAULT_DATASET_PATH) -> None:
        self.dataset_path = Path(dataset_path)

    def load(self) -> pd.DataFrame:
        """Carrega o dataset e valida sua estrutura e conteúdo."""
        if not self.dataset_path.exists():
            raise FileNotFoundError(
                f"Dataset de sentimentos não encontrado: {self.dataset_path}"
            )

        df = pd.read_csv(self.dataset_path)

        missing_columns = [
            column for column in REQUIRED_COLUMNS if column not in df.columns
        ]
        if missing_columns:
            raise ValueError(f"Colunas obrigatórias ausentes: {missing_columns}")

        if df.empty:
            raise ValueError("O dataset de sentimentos está vazio.")

        if df[REQUIRED_COLUMNS].isnull().any().any():
            raise ValueError("O dataset contém valores nulos.")

        if not df["emotion"].isin(VALID_EMOTIONS).all():
            invalid_emotions = sorted(set(df["emotion"]) - VALID_EMOTIONS)
            raise ValueError(f"Emoções inválidas encontradas: {invalid_emotions}")

        if not df["score"].between(0.0, 1.0).all():
            raise ValueError("Existem scores fora do intervalo [0, 1].")

        return df[REQUIRED_COLUMNS].copy()
