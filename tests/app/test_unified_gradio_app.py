import pandas as pd

from src.app.gradio_app import create_unified_app


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


def test_create_unified_app_returns_gradio_blocks():
    app = create_unified_app(sample_data())

    assert app is not None
    assert hasattr(app, "launch")


def test_unified_app_contains_expected_components():
    app = create_unified_app(sample_data())

    component_types = {
        component.__class__.__name__ for component in app.blocks.values()
    }

    assert "Textbox" in component_types
    assert "Button" in component_types


def test_unified_app_builds_with_sample_data():
    app = create_unified_app(sample_data())

    assert app is not None
