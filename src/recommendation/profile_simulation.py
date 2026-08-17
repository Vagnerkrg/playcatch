from dataclasses import dataclass

import pandas as pd

from src.recommendation.feedback import FeedbackTracker
from src.recommendation.recommender import MusicRecommender


@dataclass(frozen=True)
class UserProfile:
    """Representa um perfil simulado para validação do recomendador."""

    name: str
    preferred_emotion: str


PROFILES = [
    UserProfile(
        name="Perfil Alegre",
        preferred_emotion="joy",
    ),
    UserProfile(
        name="Perfil Melancólico",
        preferred_emotion="sadness",
    ),
    UserProfile(
        name="Perfil Intenso",
        preferred_emotion="anger",
    ),
]


def simulate_profile(
    data: pd.DataFrame,
    profile: UserProfile,
) -> dict[str, object]:
    """Executa uma simulação antes e depois dos feedbacks."""
    recommender_before = MusicRecommender(data)

    before = recommender_before.recommend(
        profile.preferred_emotion,
        limit=3,
    )

    if before.empty:
        raise ValueError(
            f"Nenhuma recomendação disponível para {profile.preferred_emotion}."
        )

    tracker = FeedbackTracker()

    skipped_song_id = str(before.iloc[0]["song_id"])
    tracker.skipped(skipped_song_id)

    liked_song_id = None

    if len(before) > 1:
        liked_song_id = str(before.iloc[-1]["song_id"])
        tracker.liked(liked_song_id)

    feedback = tracker.get_all()

    recommender_after = MusicRecommender(
        data,
        feedback=feedback,
    )

    after = recommender_after.recommend(
        profile.preferred_emotion,
        limit=3,
    )

    return {
        "profile": profile,
        "before": before,
        "after": after,
        "feedback": feedback,
        "skipped_song_id": skipped_song_id,
        "liked_song_id": liked_song_id,
    }


def run_simulations(data: pd.DataFrame) -> list[dict[str, object]]:
    """Executa todos os perfis simulados."""
    return [simulate_profile(data, profile) for profile in PROFILES]


def main() -> None:
    """Executa as simulações e imprime os resultados."""
    from src.recommendation.sentiment_data_loader import SentimentDataLoader

    data = SentimentDataLoader().load()
    simulations = run_simulations(data)

    for simulation in simulations:
        profile = simulation["profile"]
        before = simulation["before"]
        after = simulation["after"]
        feedback = simulation["feedback"]

        print(f"\n=== {profile.name} ===")
        print(f"Preferência: {profile.preferred_emotion}")

        print("\nAntes do feedback:")
        for row in before.itertuples():
            print(f"- {row.title} | {row.emotion} | score={row.score:.4f}")

        print("\nFeedback:")
        for interaction in feedback:
            print(f"- {interaction.song_id}: {interaction.feedback}")

        print("\nDepois do feedback:")
        for row in after.itertuples():
            print(
                f"- {row.title} | {row.emotion} | "
                f"score={row.score:.4f} | adjusted={row.adjusted_score:.4f}"
            )


if __name__ == "__main__":
    main()
