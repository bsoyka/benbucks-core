import pytest

from benbucks_core import Lottery, Pool, User


async def test_lottery_init(mongo_mock_client):
    """Test that a lottery can be created."""
    lottery = Lottery(name="test", prize=100, ticket_price=10)

    assert lottery.name == "test"
    assert lottery.prize == 100
    assert lottery.ticket_price == 10
    assert lottery.prize_increase == 0
    assert lottery.pool_increases == []
    assert lottery.tickets == []
    assert lottery.winner is None
    assert lottery.completed is False


async def test_lottery_change_prize(mongo_mock_client):
    """Test that a lottery's prize can be changed."""
    lottery = Lottery(name="test", prize=100, ticket_price=10)
    assert lottery.prize == 100

    await lottery.change_prize(10)
    await lottery.change_prize(-5)
    await lottery.change_prize(2)

    assert lottery.prize == 107


async def test_lottery_change_prize_negative(mongo_mock_client):
    """Test that a lottery's prize cannot be made negative."""
    lottery = Lottery(name="test", prize=100, ticket_price=10)
    assert lottery.prize == 100

    await lottery.change_prize(-1)
    assert lottery.prize == 99

    with pytest.raises(ValueError):
        await lottery.change_prize(-100)

    assert lottery.prize == 99


async def test_lottery_buy_ticket(mongo_mock_client):
    """Test that a lottery ticket can be bought."""
    user = User(name="test", balance=15)
    pool1 = Pool(code="test1")
    pool2 = Pool(code="test2")

    lottery = Lottery(
        name="test",
        prize=100,
        ticket_price=10,
        prize_increase=5,
        pool_increases=[(pool1, 7), (pool2, 3)],
    )

    assert lottery.prize == 100
    assert lottery.ticket_price == 10
    assert lottery.prize_increase == 5
    assert lottery.pool_increases == [(pool1, 7), (pool2, 3)]
    assert lottery.tickets == []

    await lottery.buy_ticket(user)

    assert lottery.prize == 105
    assert lottery.ticket_price == 10
    assert lottery.prize_increase == 5
    assert lottery.pool_increases == [(pool1, 7), (pool2, 3)]
    assert lottery.tickets == [user]

    assert user.balance == 5
    assert pool1.balance == 7
    assert pool2.balance == 3


async def test_lottery_buy_ticket_not_enough_money(mongo_mock_client):
    """Test that a lottery ticket cannot be bought if the user doesn't
    have enough money."""
    user = User(name="test", balance=5)
    lottery = Lottery(name="test", prize=100, ticket_price=10)

    assert lottery.prize == 100
    assert lottery.ticket_price == 10
    assert lottery.prize_increase == 0
    assert lottery.pool_increases == []
    assert lottery.tickets == []

    with pytest.raises(ValueError):
        await lottery.buy_ticket(user)

    assert lottery.prize == 100
    assert lottery.ticket_price == 10
    assert lottery.prize_increase == 0
    assert lottery.pool_increases == []
    assert lottery.tickets == []

    assert user.balance == 5


async def test_lottery_complete_one_user(mongo_mock_client):
    """Test that a lottery can be completed with one ticket."""
    user = User(name="test")
    lottery = Lottery(name="test", prize=100, ticket_price=10, tickets=[user])

    await lottery.complete()

    assert lottery.winner == user
    assert lottery.completed is True

    assert user.balance == 100


async def test_lottery_complete_multiple_users(mongo_mock_client):
    """Test that a lottery can be completed with multiple tickets."""
    user1 = User(name="test1")
    user2 = User(name="test2")
    user3 = User(name="test3")

    lottery = Lottery(
        name="test",
        prize=100,
        ticket_price=10,
        tickets=[user1, user2, user3],
    )

    await lottery.complete()

    assert lottery.winner in [user1, user2, user3]
    assert lottery.completed is True

    assert lottery.winner.balance == 100

    non_winners = [user1, user2, user3]
    non_winners.remove(lottery.winner)

    for user in non_winners:
        assert user.balance == 0


async def test_lottery_complete_no_users(mongo_mock_client):
    """Test that a lottery can be completed with no tickets."""
    lottery = Lottery(name="test", prize=100, ticket_price=10)

    await lottery.complete()

    assert lottery.winner is None
    assert lottery.completed is True


async def test_lottery_get_chance_one_user(mongo_mock_client):
    """Test that the chance of winning is correct with one ticket."""
    user = User(name="test")
    lottery = Lottery(name="test", prize=100, ticket_price=10, tickets=[user])

    assert await lottery.get_chance(user) == 1


async def test_lottery_get_chance_multiple_users(mongo_mock_client):
    """Test that the chance of winning is correct with three tickets."""
    user1 = User(name="test1")
    user2 = User(name="test2")
    user3 = User(name="test3")

    lottery = Lottery(
        name="test",
        prize=100,
        ticket_price=10,
        tickets=[user1, user2, user3],
    )

    assert await lottery.get_chance(user1) == 1 / 3
    assert await lottery.get_chance(user2) == 1 / 3
    assert await lottery.get_chance(user3) == 1 / 3


async def test_lottery_get_chance_no_users(mongo_mock_client):
    """Test that the chance of winning is correct with no tickets."""
    user = User(name="test")
    lottery = Lottery(name="test", prize=100, ticket_price=10)

    assert await lottery.get_chance(user) == 0
