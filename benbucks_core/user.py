from typing import Optional

from beanie import Document

from ._utils import _round_money


class User(Document):
    """A BenBucks user.

    Attributes:
        name (str): The user's name.
        balance (int | float, optional): The user's balance. Defaults to
            0.
        pin (str, optional): The user's PIN. Defaults to None.
    """

    name: str
    balance: int | float = 0
    pin: Optional[str] = None

    async def change_name(self, name: str) -> None:
        """Change the user's name.

        Args:
            name (str): The new name for the user.
        """
        self.name = name
        await self.save()

    async def change_balance(self, amount: int | float) -> int | float:
        """Change the user's balance by a given amount.

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
