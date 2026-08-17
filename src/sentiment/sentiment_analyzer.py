from transformers import pipeline


MODEL_NAME = "MilaNLProc/xlm-emo-t"


class SentimentAnalyzer:
    """Analisador de emoções baseado no modelo XLM-EMO."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
        )

    def analyze(self, text: str) -> dict[str, float | str]:
        """Analisa o sentimento de um texto e retorna emoção e score."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("O texto para análise não pode estar vazio.")

        result = self.classifier(text)[0]

        return {
            "emotion": result["label"],
            "score": float(result["score"]),
        }
