from pathlib import Path

import pandas as pd
import pytest

from src.app.playcatch_app import PlaycatchApp


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3", "4"],
            "title": [
                "Happy Song",
                "Joyful Song",
                "Sad Song",
                "Angry Song",
            ],
            "artist": [
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist D",
            ],
            "language": [
                "en",
                "en",
                "en",
                "de",
            ],
            "lyrics": [
                "Happy lyrics",
                "Joyful lyrics",
                "Sad lyrics",
                "Angry lyrics",
            ],
            "emotion": [
                "joy",
                "joy",
                "sadness",
                "anger",
            ],
            "score": [
                0.95,
                0.85,
                0.90,
                0.88,
            ],
        }
    )


def test_app_initializes_with_sentiment_data(sample_data):
    app = PlaycatchApp(sample_data)

    assert len(app.sentiment_data) == 4
    assert app.chatbot is not None


def test_app_recommends_from_natural_language(sample_data):
    app = PlaycatchApp(sample_data)

    response = app.recommend("Quero músicas felizes")

    assert "Happy Song" in response
    assert "Joyful Song" in response


def test_app_preserves_conversation_context(sample_data):
    app = PlaycatchApp(sample_data)

    app.recommend("Quero músicas felizes")

    response = app.recommend("Quero mais parecidas")

    assert "Happy Song" in response
    assert "joy" in response


def test_app_respects_recommendation_limit(sample_data):
    app = PlaycatchApp(sample_data)

    response = app.recommend(
        "Quero músicas felizes",
        limit=1,
    )

    assert "Happy Song" in response
    assert "Joyful Song" not in response


def test_from_csv_loads_dataset(tmp_path, sample_data):
    path = Path(tmp_path) / "lyrics_sentiment.csv"
    sample_data.to_csv(path, index=False)

    app = PlaycatchApp.from_csv(path)

    assert app.sentiment_data.shape == (4, 7)


def test_from_csv_rejects_missing_file(tmp_path):
    path = Path(tmp_path) / "missing.csv"

    with pytest.raises(
        FileNotFoundError,
        match="Dataset de sentimentos não encontrado",
    ):
        PlaycatchApp.from_csv(path)


def test_app_rejects_unrecognized_query(sample_data):
    app = PlaycatchApp(sample_data)

    with pytest.raises(
        ValueError,
        match="não foi possível identificar uma emoção",
    ):
        app.recommend("Quero músicas para estudar.")
