import pytest

from src.sentiment.sentiment_analyzer import SentimentAnalyzer


def test_analyze_returns_emotion_and_score(monkeypatch):
    def fake_pipeline(*args, **kwargs):
        def classifier(text, **kwargs):
            return [{"label": "joy", "score": 0.95}]

        return classifier

    monkeypatch.setattr(
        "src.sentiment.sentiment_analyzer.pipeline",
        fake_pipeline,
    )

    analyzer = SentimentAnalyzer()

    result = analyzer.analyze("I am happy today.")

    assert result["emotion"] == "joy"
    assert result["score"] == 0.95


def test_analyze_rejects_empty_text(monkeypatch):
    def fake_pipeline(*args, **kwargs):
        return lambda text, **kwargs: [{"label": "joy", "score": 0.95}]

    monkeypatch.setattr(
        "src.sentiment.sentiment_analyzer.pipeline",
        fake_pipeline,
    )

    analyzer = SentimentAnalyzer()

    with pytest.raises(
        ValueError,
        match="texto para análise não pode estar vazio",
    ):
        analyzer.analyze("   ")
