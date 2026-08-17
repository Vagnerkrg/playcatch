import pytest

from src.recommendation.feedback import FeedbackTracker


def test_register_liked_feedback():
    tracker = FeedbackTracker()

    interaction = tracker.liked("song-001")

    assert interaction.song_id == "song-001"
    assert interaction.feedback == "liked"
    assert interaction.timestamp
    assert tracker.count() == 1


def test_register_skipped_feedback():
    tracker = FeedbackTracker()

    interaction = tracker.skipped("song-002")

    assert interaction.song_id == "song-002"
    assert interaction.feedback == "skipped"
    assert interaction.timestamp
    assert tracker.count() == 1


def test_register_multiple_feedbacks():
    tracker = FeedbackTracker()

    tracker.liked("song-001")
    tracker.skipped("song-002")

    interactions = tracker.get_all()

    assert len(interactions) == 2
    assert interactions[0].song_id == "song-001"
    assert interactions[0].feedback == "liked"
    assert interactions[1].song_id == "song-002"
    assert interactions[1].feedback == "skipped"


def test_rejects_invalid_feedback():
    tracker = FeedbackTracker()

    with pytest.raises(ValueError, match="Feedback inválido"):
        tracker.register("song-001", "neutral")


def test_rejects_empty_song_id():
    tracker = FeedbackTracker()

    with pytest.raises(ValueError, match="song_id não pode estar vazio"):
        tracker.liked("   ")
