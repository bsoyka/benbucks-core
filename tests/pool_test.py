import pytest

from benbucks_core import Pool


def test_pool_init(mongo_mock_client):
    """Test that a pool can be created."""
    pool = Pool(code="abc")
    assert pool.code == "abc"
    assert pool.name == "Pool"
    assert pool.balance == 0.0


async def test_pool_change_balance(mongo_mock_client):
    """Test that a pool's balance can be changed."""
    pool = Pool(code="abc", name="Pool")
    assert pool.balance == 0.0

    await pool.change_balance(10.0)
    await pool.change_balance(-5.0)
    await pool.change_balance(2.0)

    assert pool.balance == 7.0


async def test_pool_change_balance_negative(mongo_mock_client):
    """Test that a pool's balance cannot be made negative."""
    pool = Pool(code="abc", name="Pool", balance=5.0)
    assert pool.balance == 5.0

    await pool.change_balance(-1.0)
    assert pool.balance == 4.0

    with pytest.raises(ValueError):
        await pool.change_balance(-5.0)

    assert pool.balance == 4.0


async def test_pool_get_by_code(mongo_mock_client):
    """Test that a pool can be retrieved by its code."""
    pool = Pool(code="abc", name="Pool")
    await pool.save()

    pool2 = await Pool.get_by_code("abc")
    assert pool2 == pool


async def test_pool_get_by_code_create(mongo_mock_client):
    """Test that a pool can be retrieved by its code, creating it if it
    does not exist."""
    pool = await Pool.get_by_code("abc")
    assert pool.code == "abc"
    assert pool.name == "Pool"
    assert pool.balance == 0.0

    pool2 = await Pool.get_by_code("abc")
    assert pool2 == pool


async def test_pool_get_by_code_error(mongo_mock_client):
    """Test that an error is raised when a pool is retrieved by its code
    and it does not exist."""
    with pytest.raises(ValueError):
        await Pool.get_by_code("abc", create_if_needed=False)
