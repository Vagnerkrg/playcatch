import re
import unicodedata
from dataclasses import dataclass

from src.recommendation.sentiment_data_loader import VALID_EMOTIONS


INTENT_RECOMMEND = "recommend"


@dataclass(frozen=True)
class QueryInterpretation:
    """Representa a interpretação estruturada de uma consulta."""

    intent: str
    emotion: str


EMOTION_KEYWORDS = {
    "joy": {
        "alegre",
        "alegres",
        "alegria",
        "feliz",
        "felizes",
        "felicidade",
        "animado",
        "animada",
        "animados",
        "animadas",
        "animacao",
        "divertido",
        "divertida",
        "divertidos",
        "divertidas",
        "positivo",
        "positiva",
        "positivos",
        "positivas",
        "upbeat",
        "happy",
        "joy",
    },
    "sadness": {
        "triste",
        "tristes",
        "tristeza",
        "melancolico",
        "melancolica",
        "melancolicos",
        "melancolicas",
        "melancolia",
        "deprimido",
        "deprimida",
        "deprimidos",
        "deprimidas",
        "baixo",
        "baixa",
        "baixos",
        "baixas",
        "down",
        "sad",
        "sadness",
    },
    "anger": {
        "raiva",
        "raivoso",
        "raivosa",
        "raivosos",
        "raivosas",
        "furioso",
        "furiosa",
        "furiosos",
        "furiosas",
        "furia",
        "irritado",
        "irritada",
        "irritados",
        "irritadas",
        "agressivo",
        "agressiva",
        "agressivos",
        "agressivas",
        "intenso",
        "intensa",
        "intensos",
        "intensas",
        "anger",
    },
    "fear": {
        "medo",
        "medos",
        "assustado",
        "assustada",
        "assustados",
        "assustadas",
        "assustador",
        "assustadora",
        "assustadores",
        "assustadoras",
        "ansioso",
        "ansiosa",
        "ansiosos",
        "ansiosas",
        "ansiedade",
        "tenso",
        "tensa",
        "tensos",
        "tensas",
        "fear",
    },
}


def _normalize_text(text: str) -> str:
    """Normaliza texto para comparação de palavras-chave."""
    normalized = unicodedata.normalize("NFKD", text)
    normalized = "".join(
        character for character in normalized if not unicodedata.combining(character)
    )
    normalized = normalized.lower()
    return re.sub(r"\s+", " ", normalized).strip()


class QueryInterpreter:
    """Interpreta consultas e mapeia linguagem natural para emoções."""

    def interpret(self, query: str) -> QueryInterpretation:
        """Transforma uma consulta em intent e emoção."""
        if not isinstance(query, str) or not query.strip():
            raise ValueError("A consulta não pode estar vazia.")

        normalized_query = _normalize_text(query)
        matches = self._find_emotions(normalized_query)

        if not matches:
            raise ValueError("não foi possível identificar uma emoção na consulta.")

        if len(matches) > 1:
            raise ValueError(
                "A consulta contém mais de uma emoção e não pode ser "
                "interpretada de forma unívoca."
            )

        return QueryInterpretation(
            intent=INTENT_RECOMMEND,
            emotion=matches[0],
        )

    @staticmethod
    def _find_emotions(query: str) -> list[str]:
        """Retorna as emoções identificadas na consulta."""
        matches = []

        for emotion in VALID_EMOTIONS:
            keywords = EMOTION_KEYWORDS[emotion]

            if any(
                re.search(rf"\b{re.escape(keyword)}\b", query) for keyword in keywords
            ):
                matches.append(emotion)

        return sorted(matches)
