import pandas as pd

from src.recommendation.feedback import Feedback
from src.recommendation.sentiment_data_loader import VALID_EMOTIONS


DEFAULT_LIMIT = 5
LIKED_BOOST = 0.10


class MusicRecommender:
    """Recomenda músicas com base na emoção e no feedback do usuário."""

    def __init__(
        self,
        data: pd.DataFrame,
        feedback: list[Feedback] | None = None,
    ) -> None:
        self.data = data.copy()
        self.feedback = feedback or []
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

    def _feedback_by_song(self) -> dict[str, str]:
        """Retorna o feedback mais recente por música."""
        feedback_by_song: dict[str, str] = {}

        for interaction in self.feedback:
            feedback_by_song[interaction.song_id] = interaction.feedback

        return feedback_by_song

    def recommend(
        self,
        emotion: str,
        limit: int = DEFAULT_LIMIT,
    ) -> pd.DataFrame:
        """Retorna recomendações ajustadas pelo histórico de feedback."""
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

        recommendations = self.data[self.data["emotion"] == emotion].copy()

        feedback_by_song = self._feedback_by_song()

        recommendations["feedback"] = recommendations["song_id"].map(feedback_by_song)

        recommendations = recommendations[
            recommendations["feedback"] != "skipped"
        ].copy()

        recommendations["adjusted_score"] = recommendations.apply(
            lambda row: min(
                row["score"] + LIKED_BOOST
                if row["feedback"] == "liked"
                else row["score"],
                1.0,
            ),
            axis=1,
        )

        recommendations = (
            recommendations.sort_values(
                by=["adjusted_score", "score", "title"],
                ascending=[False, False, True],
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
                "adjusted_score",
            ]
        ]
