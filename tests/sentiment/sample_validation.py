import pandas as pd

from src.sentiment.sentiment_analyzer import SentimentAnalyzer


df = pd.read_csv("data/processed/lyrics_clean.csv")
sample = df.groupby("language", sort=True).head(2)

analyzer = SentimentAnalyzer()

print(f"Amostra: {len(sample)} letras")
print(
    "Distribuição:",
    sample["language"].value_counts().sort_index().to_dict(),
)
print()

for row in sample.itertuples():
    result = analyzer.analyze(row.lyrics)

    print(f"[{row.language}] {row.title} — {result['emotion']} ({result['score']:.4f})")
