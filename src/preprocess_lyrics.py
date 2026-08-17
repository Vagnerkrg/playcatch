from pathlib import Path

from src.data.lyrics_loader import load_lyrics_dataset
from src.preprocessing.lyrics_cleaner import clean_lyrics_dataframe


RAW_PATH = Path("data/raw/lyrics.csv")
PROCESSED_PATH = Path("data/processed/lyrics_clean.csv")


def main() -> None:
    RAW_PATH.parent.mkdir(parents=True, exist_ok=True)
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    df = load_lyrics_dataset()
    df.to_csv(RAW_PATH, index=False)

    cleaned = clean_lyrics_dataframe(df)
    cleaned.to_csv(PROCESSED_PATH, index=False)

    print(f"Raw: {len(df)} registros")
    print(f"Processed: {len(cleaned)} registros")


if __name__ == "__main__":
    main()
