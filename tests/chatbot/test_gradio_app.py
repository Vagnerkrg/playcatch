import pandas as pd

from src.chatbot.gradio_app import create_app


def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3"],
            "title": ["Happy Song", "Joyful Song", "Sad Song"],
            "artist": ["Artist A", "Artist B", "Artist C"],
            "language": ["en", "en", "en"],
            "lyrics": ["Happy lyrics", "Joyful lyrics", "Sad lyrics"],
            "emotion": ["joy", "joy", "sadness"],
            "score": [0.95, 0.85, 0.90],
        }
    )


def test_create_app_returns_gradio_blocks():
    app = create_app(sample_data())

    assert app is not None
    assert hasattr(app, "launch")


def test_create_app_builds_without_loading_real_dataset():
    app = create_app(sample_data())

    assert app is not None
