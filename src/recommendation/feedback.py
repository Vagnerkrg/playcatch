from dataclasses import dataclass
from datetime import datetime, timezone


VALID_FEEDBACK = {"liked", "skipped"}


@dataclass(frozen=True)
class Feedback:
    """Representa uma interação do usuário com uma música."""

    song_id: str
    feedback: str
    timestamp: str


class FeedbackTracker:
    """Registra feedbacks do usuário em memória."""

    def __init__(self) -> None:
        self._interactions: list[Feedback] = []

    def register(self, song_id: str, feedback: str) -> Feedback:
        """Registra um feedback associado a uma música."""
        if not isinstance(song_id, str) or not song_id.strip():
            raise ValueError("O song_id não pode estar vazio.")

        if not isinstance(feedback, str) or feedback not in VALID_FEEDBACK:
            raise ValueError(
                f"Feedback inválido: {feedback}. "
                f"Valores aceitos: {sorted(VALID_FEEDBACK)}"
            )

        interaction = Feedback(
            song_id=song_id.strip(),
            feedback=feedback,
            timestamp=datetime.now(timezone.utc).isoformat(),
        )

        self._interactions.append(interaction)

        return interaction

    def liked(self, song_id: str) -> Feedback:
        """Registra que o usuário gostou da música."""
        return self.register(song_id, "liked")

    def skipped(self, song_id: str) -> Feedback:
        """Registra que o usuário pulou a música."""
        return self.register(song_id, "skipped")

    def get_all(self) -> list[Feedback]:
        """Retorna todas as interações registradas."""
        return list(self._interactions)

    def count(self) -> int:
        """Retorna a quantidade de interações registradas."""
        return len(self._interactions)
