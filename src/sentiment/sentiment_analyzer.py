from transformers import AutoTokenizer, pipeline


MODEL_NAME = "MilaNLProc/xlm-emo-t"
MAX_TOKENS = 480
OVERLAP_TOKENS = 64
EMOTIONS = {"anger", "fear", "joy", "sadness"}


class SentimentAnalyzer:
    """Analisador de emoções baseado no modelo XLM-EMO."""

    def __init__(self, model_name: str = MODEL_NAME) -> None:
        self.model_name = model_name
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)
        self.classifier = pipeline(
            "text-classification",
            model=model_name,
        )

    def _split_text(self, text: str) -> list[str]:
        """Divide textos longos em blocos compatíveis com o modelo."""
        token_ids = self.tokenizer.encode(
            text,
            add_special_tokens=False,
        )

        if len(token_ids) <= MAX_TOKENS:
            return [text]

        chunks = []
        step = MAX_TOKENS - OVERLAP_TOKENS

        for start in range(0, len(token_ids), step):
            chunk_ids = token_ids[start : start + MAX_TOKENS]

            if not chunk_ids:
                break

            chunk_text = self.tokenizer.decode(
                chunk_ids,
                skip_special_tokens=True,
            ).strip()

            if chunk_text:
                chunks.append(chunk_text)

            if start + MAX_TOKENS >= len(token_ids):
                break

        return chunks

    def analyze(self, text: str) -> dict[str, float | str]:
        """Analisa um texto completo e retorna emoção e score agregados."""
        if not isinstance(text, str) or not text.strip():
            raise ValueError("O texto para análise não pode estar vazio.")

        chunks = self._split_text(text)

        try:
            predictions = self.classifier(
                chunks,
                truncation=True,
                max_length=514,
                top_k=None,
            )
        except TypeError:
            predictions = self.classifier(chunks)

        if chunks and len(chunks) == 1:
            if predictions and isinstance(predictions[0], dict):
                chunk_predictions = [predictions]
            else:
                chunk_predictions = predictions
        else:
            chunk_predictions = predictions

        scores = {emotion: [] for emotion in EMOTIONS}

        for prediction_set in chunk_predictions:
            if isinstance(prediction_set, dict):
                prediction_set = [prediction_set]

            for prediction in prediction_set:
                label = prediction["label"]
                score = float(prediction["score"])

                if label in scores:
                    scores[label].append(score)

        aggregated = {
            emotion: sum(values) / len(values) if values else 0.0
            for emotion, values in scores.items()
        }

        emotion = max(aggregated, key=aggregated.get)

        return {
            "emotion": emotion,
            "score": aggregated[emotion],
        }
