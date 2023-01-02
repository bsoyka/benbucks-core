from typing import Self

from beanie import Document

from ._utils import _round_money


class Pool(Document):
    """A pool of currency that users can contribute to."""

    code: str
    name: str = "Pool"
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

    @classmethod
    async def get_by_code(
        cls, code: str, create_if_needed: bool = True
    ) -> Self:
        """Get a pool by its code.

        Args:
            code (str): The code of the pool.
            create_if_needed (bool, optional): Whether to create the
                pool if it doesn't exist. Defaults to True.

        Raises:
            ValueError: If the pool doesn't exist and create_if_needed
                is False.

        Returns:
            Pool: The pool with the given code.
        """
        pool = await cls.find_one(cls.code == code)

        if not pool:
            if create_if_needed:
                pool = cls(code=code)
                await pool.save()
            else:
                raise ValueError("Pool not found")

        return pool
