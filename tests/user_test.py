import pytest

from benbucks_core import User


@pytest.mark.asyncio
async def test_user_init(mongo_mock_client):
    """Test that a user can be created."""
    user = User(name="test")

    assert user.name == "test"
    assert user.balance == 0
    assert user.pin is None


@pytest.mark.asyncio
async def test_user_change_name(mongo_mock_client):
    """Test that a user's name can be changed."""
    user = User(name="test1")
    assert user.name == "test1"

    await user.change_name("test2")
    assert user.name == "test2"


@pytest.mark.asyncio
async def test_user_change_balance(mongo_mock_client):
    """Test that a user's balance can be changed."""
    user = User(name="test")
    assert user.balance == 0

    await user.change_balance(10)
    await user.change_balance(-5)
    await user.change_balance(2)

    assert user.balance == 7


@pytest.mark.asyncio
async def test_user_change_balance_negative(mongo_mock_client):
    """Test that a user's balance cannot be made negative."""
    user = User(name="test", balance=5)
    assert user.balance == 5

    await user.change_balance(-1)
    assert user.balance == 4

    with pytest.raises(ValueError):
        await user.change_balance(-5)

    assert user.balance == 4


@pytest.mark.asyncio
async def test_user_set_pin_from_empty(mongo_mock_client):
    """Test that a user's pin can be set when empty."""
    user = User(name="test")
    assert user.pin is None

    await user.set_pin("1234")
    assert user.pin == "1234"


@pytest.mark.asyncio
async def test_user_set_pin_with_override(mongo_mock_client):
    """Test that a user's pin can be set again using the override
    parameter."""
    user = User(name="test", pin="1234")
    assert user.pin == "1234"

    await user.set_pin("5678", override=True)
    assert user.pin == "5678"


@pytest.mark.asyncio
async def test_user_set_pin_without_override(mongo_mock_client):
    """Test that a user's pin cannot be set again without using the
    override parameter."""
    user = User(name="test", pin="1234")
    assert user.pin == "1234"

    with pytest.raises(ValueError):
        await user.set_pin("5678")

    assert user.pin == "1234"