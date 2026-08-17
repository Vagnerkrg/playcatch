import re

import pandas as pd

from src.chatbot.conversation_context import ConversationContext
from src.chatbot.query_interpreter import QueryInterpreter
from src.recommendation.recommender import MusicRecommender


FOLLOW_UP_PATTERNS = (
    r"^(mais)$",
    r"^(quero|me de|me dê) mais$",
    r"^(mais parecidas?)$",
    r"^(quero|me de|me dê) mais parecidas?$",
    r"^(outras)$",
    r"^(quero|me de|me dê) outras$",
    r"^(outras parecidas?)$",
    r"^(quero|me de|me dê) outras parecidas?$",
    r"^(mais musicas)$",
    r"^(mais músicas)$",
    r"^(quero|me de|me dê) mais musicas$",
    r"^(quero|me de|me dê) mais músicas$",
    r"^(outras musicas)$",
    r"^(outras músicas)$",
    r"^(quero|me de|me dê) outras musicas$",
    r"^(quero|me de|me dê) outras músicas$",
    r"^(parecidas?)$",
    r"^(quero|me de|me dê) parecidas?$",
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
        """Identifica consultas explícitas de continuidade."""
        normalized = " ".join(query.lower().split())

        return any(re.fullmatch(pattern, normalized) for pattern in FOLLOW_UP_PATTERNS)

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
