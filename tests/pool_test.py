import pytest

from benbucks_core import Pool


def test_pool_init(mongo_mock_client):
    """Test that a pool can be created."""
    pool = Pool(code="abc", name="Pool")
    assert pool.code == "abc"
    assert pool.name == "Pool"
    assert pool.balance == 0


async def test_pool_change_balance(mongo_mock_client):
    """Test that a pool's balance can be changed."""
    pool = Pool(code="abc", name="Pool")
    assert pool.balance == 0

    await pool.change_balance(10)
    await pool.change_balance(-5)
    await pool.change_balance(2)

    assert pool.balance == 7


async def test_pool_change_balance_negative(mongo_mock_client):
    """Test that a pool's balance cannot be made negative."""
    pool = Pool(code="abc", name="Pool", balance=5)
    assert pool.balance == 5

    await pool.change_balance(-1)
    assert pool.balance == 4

    with pytest.raises(ValueError):
        await pool.change_balance(-5)

    assert pool.balance == 4
