from typing import Optional

from beanie import Document

from .pool import Pool


class User(Document):
    """A BenBucks user.

    Attributes:
        name (str): The user's name.
        balance (float, optional): The user's balance. Defaults to
            0.
        pin (str, optional): The user's PIN. Defaults to None.
    """

    name: str
    balance: float = 0
    pin: Optional[str] = None

    async def change_name(self, name: str) -> None:
        """Change the user's name.

        Args:
            name (str): The new name for the user.
        """
        self.name = name
        await self.save()

    async def change_balance(self, amount: float) -> float:
        """Change the user's balance by a given amount.

        Args:
            amount (float): The amount to change the balance by.

        Raises:
            ValueError: If the balance would be made negative.

        Returns:
            float: The new balance.
        """
        if self.balance + amount < 0:
            raise ValueError("Balance cannot be negative")

        self.balance = round(self.balance + amount, 2)
        await self.save()

        return self.balance

    async def set_pin(self, pin: str, override: bool = False) -> None:
        """Set the user's pin.

        Args:
            pin (str): The new pin.
            override (bool, optional): Whether to override any current
                pin. Defaults to False.

        Raises:
            ValueError: If the pin is already set and override is False.
        """
        if self.pin and not override:
            raise ValueError("Pin already set")

        self.pin = pin
        await self.save()

    async def contribute_to_pool(self, pool: Pool, amount: float) -> None:
        """Contribute to a pool.

        Args:
            pool (Pool): The pool to contribute to.
            amount (float): The amount to contribute.

        Raises:
            ValueError: If the user does not have enough money.
        """
        if amount < 0:
            raise ValueError("Cannot contribute negative amount")

        if self.balance < amount:
            raise ValueError("Not enough money")

        await self.change_balance(-amount)
        await pool.change_balance(amount)

        await self.save()
        await pool.save()
