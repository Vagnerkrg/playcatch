import pandas as pd

from src.preprocessing.lyrics_cleaner import (
    clean_lyrics,
    clean_lyrics_dataframe,
)


def test_clean_lyrics_normalizes_whitespace():
    text = "  primeira   linha \r\n\r\n\r\n segunda linha  "

    result = clean_lyrics(text)

    assert result == "primeira linha \n\n segunda linha"


def test_clean_lyrics_handles_invalid_value():
    assert clean_lyrics(None) == ""


def test_clean_lyrics_dataframe_removes_empty_lyrics():
    df = pd.DataFrame(
        {
            "song_id": ["1", "2"],
            "title": ["A", "B"],
            "artist": ["X", "Y"],
            "language": ["en", "en"],
            "lyrics": ["valid lyrics", ""],
        }
    )

    result = clean_lyrics_dataframe(df)

    assert len(result) == 1
    assert result.iloc[0]["song_id"] == "1"
