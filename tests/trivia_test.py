from benbucks_core import TriviaQuestion


async def test_trivia_question_init(mongo_mock_client):
    """Test that a trivia question can be created."""
    question = TriviaQuestion(
        question="What is the answer to life, the universe, and everything?",
        answer="42",
        first_prize=100,
    )

    assert (
        question.question
        == "What is the answer to life, the universe, and everything?"
    )
    assert question.answer == "42"
    assert question.first_prize == 100


async def test_trivia_question_prizes(mongo_mock_client):
    """Test that trivia prizes are calculated correctly."""
    question = TriviaQuestion(
        question="What is the answer to life, the universe, and everything?",
        answer="42",
        first_prize=73,
    )

    assert question.prizes == (73, 51.1, 36.5)
