from beanie import Document

PRIZE_MULTIPLIERS = (1, 0.7, 0.5)


class TriviaQuestion(Document):
    """A trivia question.

    Attributes:
        question (str): The question.
        answer (str): The correct answer.
        first_prize (float): The prize for the first place winner.
    """

    question: str
    answer: str
    first_prize: float

    @property
    def prizes(self) -> tuple[int, int, int]:
        """The prizes for the first, second, and third place winners."""
        return tuple(
            round(self.first_prize * multiplier, 2)
            for multiplier in PRIZE_MULTIPLIERS
        )
