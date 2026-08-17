from pathlib import Path

import pandas as pd

from src.sentiment.sentiment_analyzer import SentimentAnalyzer


INPUT_PATH = Path("data/processed/lyrics_clean.csv")
OUTPUT_PATH = Path("data/processed/lyrics_sentiment.csv")

REQUIRED_COLUMNS = [
    "song_id",
    "title",
    "artist",
    "language",
    "lyrics",
]

RESULT_COLUMNS = REQUIRED_COLUMNS + [
    "emotion",
    "score",
]


def load_processed_lyrics() -> pd.DataFrame:
    """Carrega e valida o dataset processado da Issue #9."""
    if not INPUT_PATH.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {INPUT_PATH}")

    df = pd.read_csv(INPUT_PATH)

    missing = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    if df.empty:
        raise ValueError("O dataset processado está vazio.")

    if df[REQUIRED_COLUMNS].isnull().any().any():
        raise ValueError("Existem valores nulos no dataset processado.")

    if (df["lyrics"].str.strip() == "").any():
        raise ValueError("Existem letras vazias no dataset processado.")

    return df


def analyze_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica o modelo de sentimento a todas as letras."""
    analyzer = SentimentAnalyzer()

    results = []

    for row in df.itertuples(index=False):
        prediction = analyzer.analyze(row.lyrics)

        results.append(
            {
                "song_id": row.song_id,
                "title": row.title,
                "artist": row.artist,
                "language": row.language,
                "lyrics": row.lyrics,
                "emotion": prediction["emotion"],
                "score": prediction["score"],
            }
        )

    return pd.DataFrame(results, columns=RESULT_COLUMNS)


def validate_results(df: pd.DataFrame, expected_rows: int) -> None:
    """Valida a integridade do dataset final."""
    if len(df) != expected_rows:
        raise ValueError(
            f"Quantidade de registros inválida: {len(df)} em vez de {expected_rows}."
        )

    if df[RESULT_COLUMNS].isnull().any().any():
        raise ValueError("O resultado final contém valores nulos.")

    valid_emotions = {"anger", "fear", "joy", "sadness"}

    if not df["emotion"].isin(valid_emotions).all():
        invalid = sorted(set(df["emotion"]) - valid_emotions)
        raise ValueError(f"Emoções inválidas encontradas: {invalid}")

    if not df["score"].between(0.0, 1.0).all():
        raise ValueError("Existem scores fora do intervalo [0, 1].")

    if (df["lyrics"].str.strip() == "").any():
        raise ValueError("Existem letras vazias no resultado final.")


def main() -> None:
    """Executa o pipeline completo e salva os resultados."""
    df = load_processed_lyrics()

    print(f"Entrada: {len(df)} registros")

    results = analyze_dataset(df)

    validate_results(results, expected_rows=len(df))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    results.to_csv(OUTPUT_PATH, index=False)

    print(f"Saída: {len(results)} registros")
    print(f"Arquivo: {OUTPUT_PATH}")
    print("Pipeline concluído com sucesso.")


if __name__ == "__main__":
    main()
