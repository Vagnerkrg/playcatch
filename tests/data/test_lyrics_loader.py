import pandas as pd

from src.preprocessing.lyrics_cleaner import clean_lyrics_dataframe


def test_lyrics_dataset_contract():
    df = pd.DataFrame(
        {
            "song_id": ["001"],
            "title": ["Test Song"],
            "artist": ["Test Artist"],
            "language": ["en"],
            "lyrics": ["Some lyrics here."],
        }
    )

    result = clean_lyrics_dataframe(df)

    assert list(result.columns) == [
        "song_id",
        "title",
        "artist",
        "language",
        "lyrics",
    ]
    assert len(result) == 1
