from beanie import Document

from ._utils import _round_money


class Pool(Document):
    """A pool of currency that users can contribute to."""

    code: str
    name: str
    balance: int | float = 0

    async def change_balance(self, amount: int | float) -> int | float:
        """Change the pool's balance by a given amount.

        Args:
            amount (int | float): The amount to change the balance by.

        Raises:
            ValueError: If the balance would be made negative.

        Returns:
            float: The new balance.
        """
        if self.balance + amount < 0:
            raise ValueError("Balance cannot be negative")

        self.balance = _round_money(self.balance + amount)
        await self.save()

        return self.balance
