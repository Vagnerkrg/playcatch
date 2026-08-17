import pandas as pd
import pytest

from src.chatbot.chatbot_validation import VALIDATION_CASES, run_validation
from src.chatbot.recommendation_service import ChatbotRecommendationService


@pytest.fixture
def sample_data():
    return pd.DataFrame(
        {
            "song_id": ["1", "2", "3", "4", "5", "6", "7", "8"],
            "title": [
                "Happy A",
                "Happy B",
                "Sad A",
                "Sad B",
                "Anger A",
                "Anger B",
                "Fear A",
                "Fear B",
            ],
            "artist": [
                "Artist A",
                "Artist B",
                "Artist C",
                "Artist D",
                "Artist E",
                "Artist F",
                "Artist G",
                "Artist H",
            ],
            "language": [
                "en",
                "en",
                "en",
                "fr",
                "de",
                "de",
                "fr",
                "es",
            ],
            "lyrics": [
                "Happy lyrics A",
                "Happy lyrics B",
                "Sad lyrics A",
                "Sad lyrics B",
                "Anger lyrics A",
                "Anger lyrics B",
                "Fear lyrics A",
                "Fear lyrics B",
            ],
            "emotion": [
                "joy",
                "joy",
                "sadness",
                "sadness",
                "anger",
                "anger",
                "fear",
                "fear",
            ],
            "score": [
                0.95,
                0.85,
                0.93,
                0.82,
                0.91,
                0.81,
                0.89,
                0.79,
            ],
        }
    )


@pytest.mark.parametrize(
    ("query", "expected_emotion"),
    [
        ("Quero músicas felizes", "joy"),
        ("Me recomenda algo alegre", "joy"),
        ("Estou triste, me recomenda alguma coisa", "sadness"),
        ("Quero músicas melancólicas", "sadness"),
        ("Quero ouvir algo mais agressivo", "anger"),
        ("Quero algo assustador", "fear"),
    ],
)
def test_varied_messages_return_expected_emotion(
    sample_data,
    query,
    expected_emotion,
):
    service = ChatbotRecommendationService(sample_data)

    service.handle_query(query)

    assert service.context.get_emotion() == expected_emotion


def test_ambiguous_message_is_rejected(sample_data):
    service = ChatbotRecommendationService(sample_data)

    with pytest.raises(
        ValueError,
        match="mais de uma emoção",
    ):
        service.handle_query("Quero algo alegre mas também triste.")


def test_unrecognized_message_is_rejected(sample_data):
    service = ChatbotRecommendationService(sample_data)

    with pytest.raises(
        ValueError,
        match="não foi possível identificar uma emoção",
    ):
        service.handle_query("Quero músicas para estudar.")


def test_continuity_uses_previous_context(sample_data):
    service = ChatbotRecommendationService(sample_data)

    service.handle_query("Quero músicas felizes")

    response = service.handle_query("Quero mais parecidas")

    assert service.context.get_emotion() == "joy"
    assert "joy" in response
    assert "Happy A" in response


def test_continuity_after_emotion_change_uses_new_context(sample_data):
    service = ChatbotRecommendationService(sample_data)

    service.handle_query("Quero músicas felizes")
    service.handle_query("Quero músicas tristes")

    response = service.handle_query("Quero mais parecidas")

    assert service.context.get_emotion() == "sadness"
    assert "sadness" in response
    assert "Sad A" in response


def test_follow_up_without_context_is_rejected(sample_data):
    service = ChatbotRecommendationService(sample_data)

    with pytest.raises(
        ValueError,
        match="Não existe contexto anterior",
    ):
        service.handle_query("Quero mais parecidas")


@pytest.mark.parametrize(
    "query",
    [
        "mais agressivas",
        "quero algo mais agressivo",
        "algo mais intenso",
        "quero uma música mais triste",
    ],
)
def test_new_preferences_with_mais_are_not_follow_ups(
    sample_data,
    query,
):
    service = ChatbotRecommendationService(sample_data)

    assert not service._is_follow_up_query(query)


def test_validation_cases_cover_four_emotions():
    emotions = {case.expected_emotion for case in VALIDATION_CASES}

    assert emotions == {
        "joy",
        "sadness",
        "anger",
        "fear",
    }


def test_run_validation_returns_expected_cases(sample_data):
    results = run_validation(sample_data)

    assert len(results) == len(VALIDATION_CASES) + 1

    for result in results[:-1]:
        case = result["case"]

        assert result["context_emotion"] == case.expected_emotion
        assert result["response"]

    continuity = results[-1]

    assert continuity["case"].query == "Quero mais parecidas"
    assert continuity["context_emotion"] == "fear"
