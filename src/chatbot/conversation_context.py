from dataclasses import dataclass

from src.recommendation.sentiment_data_loader import VALID_EMOTIONS


@dataclass
class ConversationContext:
    """Armazena o contexto relevante da conversa."""

    last_emotion: str | None = None

    def set_emotion(self, emotion: str) -> None:
        """Armazena a última emoção consultada."""
        if emotion not in VALID_EMOTIONS:
            raise ValueError(f"Emoção inválida: {emotion}")

        self.last_emotion = emotion

    def get_emotion(self) -> str | None:
        """Retorna a última emoção armazenada."""
        return self.last_emotion

    def clear(self) -> None:
        """Limpa o contexto atual."""
        self.last_emotion = None
