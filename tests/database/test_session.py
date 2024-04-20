from unittest.mock import Mock, patch

import pytest

from database.session import get_async_session


@patch("database.session.async_sessionmaker")
@pytest.mark.asyncio()
async def test_get_async_session(mock_async_sessionmaker):
    """
    Check if the async_sessionmaker object was created.
    """
    mock_engine = Mock()
    result = await get_async_session(mock_engine)

    mock_async_sessionmaker.assert_called_once()
    assert result == mock_async_sessionmaker.return_value
