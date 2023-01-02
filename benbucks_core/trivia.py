from beanie import Document

from ._utils import _round_money

SECOND_PLACE_VALUE = 0.7
THIRD_PLACE_VALUE = 0.5


class TriviaQuestion(Document):
    """A trivia question."""

    question: str
    answer: str
    first_prize: int | float

    @property
    def prizes(self) -> tuple[int, int, int]:
        """The prizes for the first, second, and third place winners."""
        return (
            _round_money(self.first_prize),
            _round_money(self.first_prize * SECOND_PLACE_VALUE),
            _round_money(self.first_prize * THIRD_PLACE_VALUE),
        )
