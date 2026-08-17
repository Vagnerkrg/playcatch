import pandas as pd

from src.recommendation.sentiment_data_loader import VALID_EMOTIONS


DEFAULT_LIMIT = 5


class MusicRecommender:
    """Recomenda músicas com base na emoção informada pelo usuário."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.data = data.copy()
        self._validate_data()

    def _validate_data(self) -> None:
        """Valida o dataset recebido pelo recomendador."""
        required_columns = {
            "song_id",
            "title",
            "artist",
            "language",
            "lyrics",
            "emotion",
            "score",
        }

        missing_columns = required_columns - set(self.data.columns)

        if missing_columns:
            raise ValueError(
                f"Colunas obrigatórias ausentes: {sorted(missing_columns)}"
            )

        if self.data.empty:
            raise ValueError("O dataset de recomendação está vazio.")

        if not self.data["emotion"].isin(VALID_EMOTIONS).all():
            raise ValueError("O dataset contém emoções inválidas.")

        if not self.data["score"].between(0.0, 1.0).all():
            raise ValueError("O dataset contém scores fora do intervalo [0, 1].")

    def recommend(
        self,
        emotion: str,
        limit: int = DEFAULT_LIMIT,
    ) -> pd.DataFrame:
        """Retorna as músicas com maior score para a emoção informada."""
        if not isinstance(emotion, str) or not emotion.strip():
            raise ValueError("O sentimento não pode estar vazio.")

        emotion = emotion.strip().lower()

        if emotion not in VALID_EMOTIONS:
            raise ValueError(
                f"Sentimento inválido: {emotion}. "
                f"Valores aceitos: {sorted(VALID_EMOTIONS)}"
            )

        if not isinstance(limit, int) or isinstance(limit, bool) or limit <= 0:
            raise ValueError("O limite deve ser um inteiro positivo.")

        recommendations = (
            self.data[self.data["emotion"] == emotion]
            .sort_values(
                by=["score", "title"],
                ascending=[False, True],
            )
            .head(limit)
            .reset_index(drop=True)
        )

        return recommendations[
            [
                "song_id",
                "title",
                "artist",
                "language",
                "emotion",
                "score",
            ]
        ]
