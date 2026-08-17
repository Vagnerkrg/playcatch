from dataclasses import dataclass
from time import perf_counter

from src.app.playcatch_app import PlaycatchApp


@dataclass(frozen=True)
class UsabilityCase:
    """Caso de validação ponta a ponta."""

    name: str
    query: str
    expected_emotion: str


VALIDATION_CASES = [
    UsabilityCase(
        name="Alegria",
        query="Quero músicas felizes",
        expected_emotion="joy",
    ),
    UsabilityCase(
        name="Tristeza",
        query="Quero músicas melancólicas",
        expected_emotion="sadness",
    ),
    UsabilityCase(
        name="Raiva",
        query="Quero ouvir algo agressivo",
        expected_emotion="anger",
    ),
    UsabilityCase(
        name="Medo",
        query="Quero algo assustador",
        expected_emotion="fear",
    ),
]


def run_usability_validation(app: PlaycatchApp) -> list[dict[str, object]]:
    """Executa casos funcionais e registra o tempo de resposta."""
    results = []

    for case in VALIDATION_CASES:
        start = perf_counter()

        response = app.recommend(
            case.query,
            limit=3,
        )

        elapsed = perf_counter() - start

        emotion = app.chatbot.context.get_emotion()

        results.append(
            {
                "case": case,
                "response": response,
                "emotion": emotion,
                "elapsed_seconds": elapsed,
            }
        )

    return results


def run_stability_validation(
    app: PlaycatchApp,
    query: str = "Quero músicas felizes",
    repetitions: int = 20,
) -> dict[str, object]:
    """Executa a mesma consulta repetidamente para validar estabilidade."""
    if repetitions <= 0:
        raise ValueError("O número de repetições deve ser positivo.")

    responses = []
    durations = []

    for _ in range(repetitions):
        start = perf_counter()

        response = app.recommend(
            query,
            limit=3,
        )

        durations.append(perf_counter() - start)
        responses.append(response)

    return {
        "repetitions": repetitions,
        "successful_runs": len(responses),
        "all_successful": len(responses) == repetitions,
        "consistent_response": len(set(responses)) == 1,
        "min_seconds": min(durations),
        "max_seconds": max(durations),
        "average_seconds": sum(durations) / len(durations),
    }


def main() -> None:
    """Executa a validação de usabilidade e estabilidade."""
    app = PlaycatchApp.from_csv()

    print("=== VALIDAÇÃO DE USABILIDADE ===")

    results = run_usability_validation(app)

    for result in results:
        case = result["case"]

        print(f"\n[{case.name}]")
        print(f"Consulta: {case.query}")
        print(f"Esperado: {case.expected_emotion}")
        print(f"Identificado: {result['emotion']}")
        print(f"Tempo: {result['elapsed_seconds']:.4f}s")

        print("Resposta:")
        print(result["response"])

    print("\n=== VALIDAÇÃO DE ESTABILIDADE ===")

    stability = run_stability_validation(app)

    print(f"Repetições: {stability['repetitions']}")
    print(f"Execuções concluídas: {stability['successful_runs']}")
    print(f"Todas bem-sucedidas: {stability['all_successful']}")
    print(f"Respostas consistentes: {stability['consistent_response']}")
    print(f"Tempo mínimo: {stability['min_seconds']:.4f}s")
    print(f"Tempo máximo: {stability['max_seconds']:.4f}s")
    print(f"Tempo médio: {stability['average_seconds']:.4f}s")


if __name__ == "__main__":
    main()
