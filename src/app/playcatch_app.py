from pathlib import Path

import pandas as pd

from src.chatbot.recommendation_service import ChatbotRecommendationService


DEFAULT_SENTIMENT_PATH = Path("data/processed/lyrics_sentiment.csv")


class PlaycatchApp:
    """Orquestra os componentes principais do Playcatch."""

    def __init__(
        self,
        sentiment_data: pd.DataFrame,
    ) -> None:
        self.sentiment_data = sentiment_data.copy()
        self.chatbot = ChatbotRecommendationService(self.sentiment_data)

    @classmethod
    def from_csv(
        cls,
        path: Path = DEFAULT_SENTIMENT_PATH,
    ) -> "PlaycatchApp":
        """Cria a aplicação carregando o dataset de sentimentos."""
        if not path.exists():
            raise FileNotFoundError(f"Dataset de sentimentos não encontrado: {path}")

        data = pd.read_csv(path)

        return cls(data)

    def recommend(
        self,
        query: str,
        limit: int = 5,
    ) -> str:
        """Processa uma consulta ponta a ponta."""
        return self.chatbot.handle_query(
            query,
            limit=limit,
        )
