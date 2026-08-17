import pytest

from src.chatbot.query_interpreter import QueryInterpreter


@pytest.fixture
def interpreter():
    return QueryInterpreter()


@pytest.mark.parametrize(
    ("query", "expected_emotion"),
    [
        ("Quero músicas felizes", "joy"),
        ("Me recomenda algo alegre", "joy"),
        ("Estou triste, me recomenda alguma coisa", "sadness"),
        ("Quero músicas melancólicas", "sadness"),
        ("Quero ouvir algo mais agressivo", "anger"),
        ("Estou com raiva, quero música intensa", "anger"),
        ("Estou com medo, me sugira músicas", "fear"),
        ("Quero algo assustador", "fear"),
    ],
)
def test_interprets_emotion_variations(
    interpreter,
    query,
    expected_emotion,
):
    result = interpreter.interpret(query)

    assert result.intent == "recommend"
    assert result.emotion == expected_emotion


def test_normalizes_accents_and_case(interpreter):
    result = interpreter.interpret("QUERO MÚSICAS FELIZES")

    assert result.intent == "recommend"
    assert result.emotion == "joy"


def test_interprets_english_emotion_keyword(interpreter):
    result = interpreter.interpret("I want something happy.")

    assert result.intent == "recommend"
    assert result.emotion == "joy"


def test_rejects_empty_query(interpreter):
    with pytest.raises(
        ValueError,
        match="consulta não pode estar vazia",
    ):
        interpreter.interpret("   ")


def test_rejects_unrecognized_query(interpreter):
    with pytest.raises(
        ValueError,
        match="não foi possível identificar uma emoção",
    ):
        interpreter.interpret("Quero ouvir músicas para estudar.")


def test_rejects_ambiguous_query(interpreter):
    with pytest.raises(
        ValueError,
        match="mais de uma emoção",
    ):
        interpreter.interpret("Quero algo alegre mas também triste.")
