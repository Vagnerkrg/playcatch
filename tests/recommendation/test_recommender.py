import pandas as pd
import pytest

from src.recommendation.recommender import MusicRecommender


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3", "4"],
            "title": ["Song A", "Song B", "Song C", "Song D"],
            "artist": ["Artist A", "Artist B", "Artist C", "Artist D"],
            "language": ["en", "en", "de", "fr"],
            "lyrics": ["Lyrics A", "Lyrics B", "Lyrics C", "Lyrics D"],
            "emotion": ["joy", "joy", "sadness", "anger"],
            "score": [0.95, 0.80, 0.90, 0.85],
        }
    )


def test_recommend_filters_by_emotion(sample_data):
    recommender = MusicRecommender(sample_data)

    result = recommender.recommend("joy")

    assert len(result) == 2
    assert result["emotion"].tolist() == ["joy", "joy"]


def test_recommend_orders_by_score(sample_data):
    recommender = MusicRecommender(sample_data)

    result = recommender.recommend("joy")

    assert result.iloc[0]["title"] == "Song A"
    assert result.iloc[0]["score"] == 0.95


def test_recommend_respects_limit(sample_data):
    recommender = MusicRecommender(sample_data)

    result = recommender.recommend("joy", limit=1)

    assert len(result) == 1
    assert result.iloc[0]["title"] == "Song A"


def test_recommend_returns_empty_for_no_match(sample_data):
    data = sample_data[sample_data["emotion"] != "fear"]

    result = MusicRecommender(data).recommend("fear")

    assert result.empty


def test_recommend_rejects_invalid_emotion(sample_data):
    recommender = MusicRecommender(sample_data)

    with pytest.raises(ValueError, match="Sentimento inválido"):
        recommender.recommend("neutral")


def test_recommend_rejects_invalid_limit(sample_data):
    recommender = MusicRecommender(sample_data)

    with pytest.raises(ValueError, match="inteiro positivo"):
        recommender.recommend("joy", limit=0)


def test_recommend_rejects_empty_emotion(sample_data):
    recommender = MusicRecommender(sample_data)

    with pytest.raises(
        ValueError,
        match="sentimento não pode estar vazio",
    ):
        recommender.recommend("   ")
