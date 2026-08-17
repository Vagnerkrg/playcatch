import pandas as pd

from src.recommendation.profile_simulation import (
    PROFILES,
    UserProfile,
    run_simulations,
    simulate_profile,
)


def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3", "4", "5", "6"],
            "title": [
                "Joy A",
                "Joy B",
                "Joy C",
                "Sad A",
                "Sad B",
                "Anger A",
            ],
            "artist": [
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist D",
                "Artist E",
                "Artist F",
            ],
            "language": [
                "en",
                "en",
                "es",
                "fr",
                "de",
                "de",
            ],
            "lyrics": [
                "Lyrics A",
                "Lyrics B",
                "Lyrics C",
                "Lyrics D",
                "Lyrics E",
                "Lyrics F",
            ],
            "emotion": [
                "joy",
                "joy",
                "joy",
                "sadness",
                "sadness",
                "anger",
            ],
            "score": [
                0.95,
                0.85,
                0.75,
                0.90,
                0.80,
                0.88,
            ],
        }
    )


def test_profile_simulation_applies_feedback():
    data = sample_data()

    profile = UserProfile(
        name="Teste",
        preferred_emotion="joy",
    )

    result = simulate_profile(data, profile)

    before_ids = result["before"]["song_id"].tolist()
    after_ids = result["after"]["song_id"].tolist()

    assert result["skipped_song_id"] == before_ids[0]
    assert result["skipped_song_id"] not in after_ids
    assert result["liked_song_id"] in before_ids


def test_profile_simulation_uses_expected_emotion():
    data = sample_data()

    profile = UserProfile(
        name="Teste",
        preferred_emotion="sadness",
    )

    result = simulate_profile(data, profile)

    assert set(result["before"]["emotion"]) == {"sadness"}
    assert set(result["after"]["emotion"]) == {"sadness"}


def test_profile_simulation_returns_feedback_history():
    data = sample_data()

    profile = UserProfile(
        name="Teste",
        preferred_emotion="joy",
    )

    result = simulate_profile(data, profile)

    feedback = result["feedback"]

    assert len(feedback) == 2
    assert {item.feedback for item in feedback} == {
        "liked",
        "skipped",
    }


def test_run_simulations_executes_all_profiles():
    data = sample_data()

    results = run_simulations(data)

    assert len(results) == len(PROFILES)

    simulated_profiles = {result["profile"].name for result in results}
    expected_profiles = {profile.name for profile in PROFILES}

    assert simulated_profiles == expected_profiles


def test_profiles_have_valid_preferences():
    valid_emotions = {
        "anger",
        "fear",
        "joy",
        "sadness",
    }

    assert all(profile.preferred_emotion in valid_emotions for profile in PROFILES)
