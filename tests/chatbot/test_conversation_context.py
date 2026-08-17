import pytest

from src.chatbot.conversation_context import ConversationContext


def test_context_starts_empty():
    context = ConversationContext()

    assert context.get_emotion() is None


def test_context_stores_last_emotion():
    context = ConversationContext()

    context.set_emotion("joy")

    assert context.get_emotion() == "joy"


def test_context_updates_last_emotion():
    context = ConversationContext()

    context.set_emotion("joy")
    context.set_emotion("sadness")

    assert context.get_emotion() == "sadness"


def test_context_rejects_invalid_emotion():
    context = ConversationContext()

    with pytest.raises(ValueError, match="Emoção inválida"):
        context.set_emotion("neutral")


def test_context_can_be_cleared():
    context = ConversationContext()

    context.set_emotion("joy")
    context.clear()

    assert context.get_emotion() is None
