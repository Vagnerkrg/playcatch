from dataclasses import dataclass

import pandas as pd

from src.chatbot.recommendation_service import ChatbotRecommendationService


@dataclass(frozen=True)
class ValidationCase:
    """Representa um caso de validação do chatbot."""

    name: str
    query: str
    expected_emotion: str


VALIDATION_CASES = [
    ValidationCase(
        name="Alegria direta",
        query="Quero músicas felizes",
        expected_emotion="joy",
    ),
    ValidationCase(
        name="Alegria por sinônimo",
        query="Me recomenda algo alegre",
        expected_emotion="joy",
    ),
    ValidationCase(
        name="Tristeza direta",
        query="Estou triste, me recomenda alguma coisa",
        expected_emotion="sadness",
    ),
    ValidationCase(
        name="Tristeza por sinônimo",
        query="Quero músicas melancólicas",
        expected_emotion="sadness",
    ),
    ValidationCase(
        name="Raiva por contexto",
        query="Quero ouvir algo mais agressivo",
        expected_emotion="anger",
    ),
    ValidationCase(
        name="Medo por contexto",
        query="Quero algo assustador",
        expected_emotion="fear",
    ),
]


def run_validation(
    data: pd.DataFrame,
) -> list[dict[str, object]]:
    """Executa casos variados e valida a continuidade da conversa."""
    service = ChatbotRecommendationService(data)
    results = []

    for case in VALIDATION_CASES:
        response = service.handle_query(case.query, limit=3)

        results.append(
            {
                "case": case,
                "response": response,
                "context_emotion": service.context.get_emotion(),
            }
        )

    continuity_response = service.handle_query(
        "Quero mais parecidas",
        limit=3,
    )

    results.append(
        {
            "case": ValidationCase(
                name="Continuidade",
                query="Quero mais parecidas",
                expected_emotion=service.context.get_emotion(),
            ),
            "response": continuity_response,
            "context_emotion": service.context.get_emotion(),
        }
    )

    return results


def main() -> None:
    """Executa a validação e imprime os resultados."""
    from src.recommendation.sentiment_data_loader import SentimentDataLoader

    data = SentimentDataLoader().load()
    results = run_validation(data)

    for result in results:
        case = result["case"]

        print(f"\n=== {case.name} ===")
        print(f"Consulta: {case.query}")
        print(f"Emoção esperada: {case.expected_emotion}")
        print(f"Contexto atual: {result['context_emotion']}")
        print("Resposta:")
        print(result["response"])


if __name__ == "__main__":
    main()
