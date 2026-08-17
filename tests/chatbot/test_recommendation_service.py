import pandas as pd
import pytest

from src.chatbot.conversation_context import ConversationContext
from src.chatbot.recommendation_service import ChatbotRecommendationService


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3", "4", "5"],
            "title": [
                "Happy Song",
                "Joyful Song",
                "Sad Song",
                "Melancholic Song",
                "Angry Song",
            ],
            "artist": [
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist D",
                "Artist E",
            ],
            "language": [
                "en",
                "en",
                "en",
                "fr",
                "en",
            ],
            "lyrics": [
                "Happy lyrics",
                "Joyful lyrics",
                "Sad lyrics",
                "Melancholic lyrics",
                "Angry lyrics",
            ],
            "emotion": [
                "joy",
                "joy",
                "sadness",
                "sadness",
                "anger",
            ],
            "score": [
                0.95,
                0.85,
                0.90,
                0.80,
                0.88,
            ],
        }
    )


def test_handle_query_returns_recommendations(sample_data):
    service = ChatbotRecommendationService(sample_data)

    response = service.handle_query("Quero músicas felizes")

    assert "Happy Song" in response
    assert "Artist A" in response
    assert "Joyful Song" in response
    assert "joy" in response


def test_handle_query_maps_natural_language_to_emotion(sample_data):
    service = ChatbotRecommendationService(sample_data)

    response = service.handle_query("Estou triste, me recomenda alguma coisa")

    assert "Sad Song" in response
    assert "Artist C" in response


def test_handle_query_respects_limit(sample_data):
    service = ChatbotRecommendationService(sample_data)

    response = service.handle_query(
        "Quero músicas felizes",
        limit=1,
    )

    assert "Happy Song" in response
    assert "Joyful Song" not in response


def test_handle_query_formats_ranked_results(sample_data):
    service = ChatbotRecommendationService(sample_data)

    response = service.handle_query("Quero músicas felizes")

    assert "1. Happy Song — Artist A (score: 0.95)" in response
    assert "2. Joyful Song — Artist B (score: 0.85)" in response


def test_handle_query_returns_message_when_no_results(sample_data):
    data = sample_data[sample_data["emotion"] != "fear"].copy()
    service = ChatbotRecommendationService(data)

    response = service.handle_query("Quero músicas assustadoras")

    assert response == "Não encontrei músicas para a emoção 'fear'."


def test_handle_query_propagates_unrecognized_query_error(sample_data):
    service = ChatbotRecommendationService(sample_data)

    with pytest.raises(
        ValueError,
        match="não foi possível identificar uma emoção",
    ):
        service.handle_query("Quero músicas para estudar.")


def test_handle_query_propagates_ambiguous_query_error(sample_data):
    service = ChatbotRecommendationService(sample_data)

    with pytest.raises(
        ValueError,
        match="mais de uma emoção",
    ):
        service.handle_query("Quero algo alegre mas também triste.")


def test_context_stores_last_emotion(sample_data):
    context = ConversationContext()
    service = ChatbotRecommendationService(
        sample_data,
        context=context,
    )

    service.handle_query("Quero músicas felizes")

    assert context.get_emotion() == "joy"


def test_follow_up_query_uses_previous_context(sample_data):
    context = ConversationContext()
    service = ChatbotRecommendationService(
        sample_data,
        context=context,
    )

    service.handle_query("Quero músicas felizes")
    response = service.handle_query("Quero mais parecidas")

    assert "Happy Song" in response
    assert "Joyful Song" in response
    assert "joy" in response


def test_new_emotion_replaces_previous_context(sample_data):
    context = ConversationContext()
    service = ChatbotRecommendationService(
        sample_data,
        context=context,
    )

    service.handle_query("Quero músicas felizes")
    service.handle_query("Quero músicas tristes")

    assert context.get_emotion() == "sadness"


def test_follow_up_without_context_is_rejected(sample_data):
    service = ChatbotRecommendationService(sample_data)

    with pytest.raises(
        ValueError,
        match="Não existe contexto anterior",
    ):
        service.handle_query("Quero mais parecidas")


def test_different_follow_up_forms_use_context(sample_data):
    context = ConversationContext()
    service = ChatbotRecommendationService(
        sample_data,
        context=context,
    )

    service.handle_query("Quero músicas felizes")

    for query in [
        "mais",
        "outras",
        "parecidas",
        "quero mais músicas",
    ]:
        response = service.handle_query(query)

        assert "joy" in response
