import pytest

from benbucks_core import Lottery, Pool, User


async def test_lottery_init(mongo_mock_client):
    """Test that a lottery can be created."""
    lottery = Lottery(name="test", prize=100.0, ticket_price=10.0)

    assert lottery.name == "test"
    assert lottery.prize == 100.0
    assert lottery.ticket_price == 10.0
    assert lottery.prize_increase == 0.0
    assert lottery.pool_increases == []
    assert lottery.tickets == []
    assert lottery.winner is None
    assert lottery.completed is False


async def test_lottery_change_prize(mongo_mock_client):
    """Test that a lottery's prize can be changed."""
    lottery = Lottery(name="test", prize=100.0, ticket_price=10.0)
    assert lottery.prize == 100.0

    await lottery.change_prize(10.0)
    await lottery.change_prize(-5.0)
    await lottery.change_prize(2.0)

    assert lottery.prize == 107.0


async def test_lottery_change_prize_negative(mongo_mock_client):
    """Test that a lottery's prize cannot be made negative."""
    lottery = Lottery(name="test", prize=100.0, ticket_price=10.0)
    assert lottery.prize == 100.0

    await lottery.change_prize(-1.0)
    assert lottery.prize == 99.0

    with pytest.raises(ValueError):
        await lottery.change_prize(-100.0)

    assert lottery.prize == 99.0


async def test_lottery_buy_ticket(mongo_mock_client):
    """Test that a lottery ticket can be bought."""
    user = User(name="test", balance=15.0)
    pool1 = Pool(code="test1")
    pool2 = Pool(code="test2")

    lottery = Lottery(
        name="test",
        prize=100.0,
        ticket_price=10.0,
        prize_increase=5.0,
        pool_increases=[(pool1, 7.0), (pool2, 3.0)],
    )

    assert lottery.prize == 100.0
    assert lottery.ticket_price == 10.0
    assert lottery.prize_increase == 5.0
    assert lottery.pool_increases == [(pool1, 7.0), (pool2, 3.0)]
    assert lottery.tickets == []

    await lottery.buy_ticket(user)

    assert lottery.prize == 105.0
    assert lottery.ticket_price == 10.0
    assert lottery.prize_increase == 5.0
    assert lottery.pool_increases == [(pool1, 7.0), (pool2, 3.0)]
    assert lottery.tickets == [user]

    assert user.balance == 5.0
    assert pool1.balance == 7.0
    assert pool2.balance == 3.0


async def test_lottery_buy_ticket_not_enough_money(mongo_mock_client):
    """Test that a lottery ticket cannot be bought if the user doesn't
    have enough money."""
    user = User(name="test", balance=5.0)
    lottery = Lottery(name="test", prize=100.0, ticket_price=10.0)

    assert lottery.prize == 100.0
    assert lottery.ticket_price == 10.0
    assert lottery.prize_increase == 0.0
    assert lottery.pool_increases == []
    assert lottery.tickets == []

    with pytest.raises(ValueError):
        await lottery.buy_ticket(user)

    assert lottery.prize == 100.0
    assert lottery.ticket_price == 10.0
    assert lottery.prize_increase == 0.0
    assert lottery.pool_increases == []
    assert lottery.tickets == []

    assert user.balance == 5.0


async def test_lottery_complete_one_user(mongo_mock_client):
    """Test that a lottery can be completed with one ticket."""
    user = User(name="test")
    lottery = Lottery(
        name="test", prize=100.0, ticket_price=10.0, tickets=[user]
    )

    await lottery.complete()

    assert lottery.winner == user
    assert lottery.completed is True

    assert user.balance == 100.0


async def test_lottery_complete_multiple_users(mongo_mock_client):
    """Test that a lottery can be completed with multiple tickets."""
    user1 = User(name="test1")
    user2 = User(name="test2")
    user3 = User(name="test3")

    lottery = Lottery(
        name="test",
        prize=100.0,
        ticket_price=10.0,
        tickets=[user1, user2, user3],
    )

    await lottery.complete()

    assert lottery.winner in [user1, user2, user3]
    assert lottery.completed is True

    assert lottery.winner.balance == 100.0

    non_winners = [user1, user2, user3]
    non_winners.remove(lottery.winner)

    for user in non_winners:
        assert user.balance == 0.0


async def test_lottery_complete_no_users(mongo_mock_client):
    """Test that a lottery can be completed with no tickets."""
    lottery = Lottery(name="test", prize=100.0, ticket_price=10.0)

    await lottery.complete()

    assert lottery.winner is None
    assert lottery.completed is True


async def test_lottery_get_chance_one_user(mongo_mock_client):
    """Test that the chance of winning is correct with one ticket."""
    user = User(name="test")
    lottery = Lottery(
        name="test", prize=100.0, ticket_price=10.0, tickets=[user]
    )

    assert await lottery.get_chance(user) == 1.0


async def test_lottery_get_chance_multiple_users(mongo_mock_client):
    """Test that the chance of winning is correct with three tickets."""
    user1 = User(name="test1")
    user2 = User(name="test2")
    user3 = User(name="test3")

    lottery = Lottery(
        name="test",
        prize=100.0,
        ticket_price=10.0,
        tickets=[user1, user2, user3],
    )

    assert await lottery.get_chance(user1) == 1 / 3
    assert await lottery.get_chance(user2) == 1 / 3
    assert await lottery.get_chance(user3) == 1 / 3


async def test_lottery_get_chance_no_users(mongo_mock_client):
    """Test that the chance of winning is correct with no tickets."""
    user = User(name="test")
    lottery = Lottery(name="test", prize=100.0, ticket_price=10.0)

    assert await lottery.get_chance(user) == 0.0
