from beanie import Document

from ._utils import _round_money

PRIZE_MULTIPLIERS = (1, 0.7, 0.5)


class TriviaQuestion(Document):
    """A trivia question.

    Attributes:
        question (str): The question.
        answer (str): The correct answer.
        first_prize (int | float): The prize for the first place winner.
    """

    question: str
    answer: str
    first_prize: int | float

    @property
    def prizes(self) -> tuple[int, int, int]:
        """The prizes for the first, second, and third place winners."""
        return tuple(
            _round_money(self.first_prize * multiplier)
            for multiplier in PRIZE_MULTIPLIERS
        )
