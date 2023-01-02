import secrets
from typing import Optional

from beanie import Document

from .pool import Pool
from .user import User


class Lottery(Document):
    """A lottery event.

    Attributes:
        name (str): The name of the lottery.
        prize (float): The prize for the lottery.
        ticket_price (float): The price of each ticket.
        prize_increase (float, optional): The amount the prize
            increases by each time a ticket is bought. Defaults to 0.
        pool_increases (list, optional): A list containing tuples, each
            containing a Pool and the amount it increases by each time a
            ticket is bought. Defaults to an empty set.
        tickets (list[User], optional): The users who have bought
            tickets. Defaults to an empty list.
        winner (User, optional): The winner of the lottery. Defaults to
            None.
        completed (bool, optional): Whether the lottery has been
            completed. Defaults to False.
    """

    name: str
    prize: float
    ticket_price: float
    prize_increase: float = 0
    pool_increases: list[tuple[Pool, float]] = []
    tickets: list[User] = []
    winner: Optional[User] = None
    completed: bool = False

    async def change_prize(self, amount: float) -> float:
        """Change the prize by a given amount.

        Args:
            amount (float): The amount to change the prize by.

        Raises:
            ValueError: If the prize would be made negative.

        Returns:
            float: The new prize.
        """
        if self.prize + amount < 0:
            raise ValueError("Prize cannot be negative")

        self.prize += amount
        await self.save()

        return self.prize

    async def buy_ticket(self, user: User) -> None:
        """Buy a ticket for the lottery.

        Args:
            user (User): The user buying the ticket.

        Raises:
            ValueError: If the user doesn't have enough money.
        """
        if user.balance < self.ticket_price:
            raise ValueError("Not enough money")

        await user.change_balance(-self.ticket_price)
        self.tickets.append(user)

        self.prize += self.prize_increase

        for pool, increase in self.pool_increases:
            pool.balance += increase
            await pool.save()

        await self.save()

    async def complete(self) -> Optional[User]:
        """Complete the lottery.

        Returns:
            User: The winner of the lottery, if any tickets were bought.
        """
        if self.tickets:
            self.winner = secrets.choice(self.tickets)
            await self.winner.change_balance(self.prize)
        else:
            self.winner = None

        self.completed = True

        await self.save()

        return self.winner

    async def get_chance(self, user: User) -> float:
        """Get the chance of the user winning the lottery.

        Args:
            user (User): The user.

        Returns:
            float: The chance of the user winning the lottery.
        """
        return (
            self.tickets.count(user) / len(self.tickets) if self.tickets else 0
        )
