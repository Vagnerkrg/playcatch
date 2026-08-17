import pandas as pd

from src.chatbot.query_interpreter import QueryInterpreter
from src.recommendation.recommender import MusicRecommender


class ChatbotRecommendationService:
    """Orquestra consulta, interpretação e recomendação."""

    def __init__(self, data: pd.DataFrame) -> None:
        self.interpreter = QueryInterpreter()
        self.recommender = MusicRecommender(data)

    def handle_query(self, query: str, limit: int = 5) -> str:
        """Processa uma consulta e retorna uma resposta formatada."""
        interpretation = self.interpreter.interpret(query)

        if interpretation.intent != "recommend":
            raise ValueError(f"Intent não suportada: {interpretation.intent}")

        recommendations = self.recommender.recommend(
            interpretation.emotion,
            limit=limit,
        )

        return self._format_response(
            interpretation.emotion,
            recommendations,
        )

    @staticmethod
    def _format_response(
        emotion: str,
        recommendations: pd.DataFrame,
    ) -> str:
        """Formata as recomendações para apresentação ao usuário."""
        if recommendations.empty:
            return f"Não encontrei músicas para a emoção '{emotion}'."

        lines = [
            f"Encontrei estas músicas para '{emotion}':",
            "",
        ]

        for index, row in enumerate(
            recommendations.itertuples(),
            start=1,
        ):
            lines.append(
                f"{index}. {row.title} — {row.artist} (score: {row.score:.2f})"
            )

        return "\n".join(lines)
