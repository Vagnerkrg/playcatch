import pandas as pd
import pytest

from src.app.playcatch_app import PlaycatchApp
from src.app.usability_validation import (
    VALIDATION_CASES,
    run_stability_validation,
    run_usability_validation,
)


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "title": [
                "Happy A",
                "Happy B",
                "Sad A",
                "Sad B",
                "Anger A",
                "Anger B",
                "Fear A",
                "Fear B",
            ],
            "artist": [
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist D",
                "Artist E",
                "Artist F",
                "Artist G",
                "Artist H",
            ],
            "language": [
                "en",
                "en",
                "en",
                "fr",
                "de",
                "de",
                "fr",
                "es",
            ],
            "lyrics": [
                "Happy lyrics A",
                "Happy lyrics B",
                "Sad lyrics A",
                "Sad lyrics B",
                "Anger lyrics A",
                "Anger lyrics B",
                "Fear lyrics A",
                "Fear lyrics B",
            ],
            "emotion": [
                "joy",
                "joy",
                "sadness",
                "sadness",
                "anger",
                "anger",
                "fear",
                "fear",
            ],
            "score": [
                0.95,
                0.85,
                0.93,
                0.82,
                0.91,
                0.81,
                0.89,
                0.79,
            ],
        }
    )


def test_usability_cases_cover_all_emotions():
    emotions = {case.expected_emotion for case in VALIDATION_CASES}

    assert emotions == {
        "joy",
        "sadness",
        "anger",
        "fear",
    }


def test_run_usability_validation_returns_all_cases(
    sample_data,
):
    app = PlaycatchApp(sample_data)

    results = run_usability_validation(app)

    assert len(results) == len(VALIDATION_CASES)

    for result in results:
        case = result["case"]

        assert result["emotion"] == case.expected_emotion
        assert result["response"]
        assert result["elapsed_seconds"] >= 0


def test_usability_responses_are_coherent(sample_data):
    app = PlaycatchApp(sample_data)

    results = run_usability_validation(app)

    for result in results:
        case = result["case"]

        assert case.expected_emotion in result["response"]


def test_stability_validation_succeeds(sample_data):
    app = PlaycatchApp(sample_data)

    result = run_stability_validation(
        app,
        repetitions=20,
    )

    assert result["repetitions"] == 20
    assert result["successful_runs"] == 20
    assert result["all_successful"] is True
    assert result["consistent_response"] is True


def test_stability_rejects_invalid_repetitions(sample_data):
    app = PlaycatchApp(sample_data)

    with pytest.raises(
        ValueError,
        match="número de repetições deve ser positivo",
    ):
        run_stability_validation(
            app,
            repetitions=0,
        )
