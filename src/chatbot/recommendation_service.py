import re

import pandas as pd

from src.chatbot.conversation_context import ConversationContext
from src.chatbot.query_interpreter import QueryInterpreter
from src.recommendation.recommender import MusicRecommender


FOLLOW_UP_PATTERNS = (
    r"\bmais\b",
    r"\bmais parecidas?\b",
    r"\bmais musicas\b",
    r"\bmais músicas\b",
    r"\boutras\b",
    r"\boutras parecidas?\b",
    r"\boutras musicas\b",
    r"\boutras músicas\b",
    r"\bparecidas?\b",
)


class ChatbotRecommendationService:
    """Orquestra consulta, interpretação, contexto e recomendação."""

    def __init__(
        self,
        data: pd.DataFrame,
        context: ConversationContext | None = None,
    ) -> None:
        self.interpreter = QueryInterpreter()
        self.recommender = MusicRecommender(data)
        self.context = context or ConversationContext()

    def handle_query(self, query: str, limit: int = 5) -> str:
        """Processa uma consulta utilizando o contexto da conversa."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("A consulta não pode estar vazia.")

        if self._is_follow_up_query(query):
            emotion = self.context.get_emotion()

            if emotion is None:
                raise ValueError("Não existe contexto anterior para esta consulta.")
        else:
            interpretation = self.interpreter.interpret(query)

            if interpretation.intent != "recommend":
                raise ValueError(f"Intent não suportada: {interpretation.intent}")

            emotion = interpretation.emotion
            self.context.set_emotion(emotion)

        recommendations = self.recommender.recommend(
            emotion,
            limit=limit,
        )

        return self._format_response(
            emotion,
            recommendations,
        )

    @staticmethod
    def _is_follow_up_query(query: str) -> bool:
        """Identifica consultas que dependem do contexto anterior."""
        normalized = " ".join(query.lower().split())

        return any(re.search(pattern, normalized) for pattern in FOLLOW_UP_PATTERNS)

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
