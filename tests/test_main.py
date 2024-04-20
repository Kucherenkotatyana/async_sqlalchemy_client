from unittest.mock import AsyncMock, Mock, patch

import pytest
from asyncpg.exceptions import DataError
from pydantic import ValidationError
from sqlalchemy.exc import DBAPIError

from main import user_service_add, user_service_get


@patch("main.get_async_session")
@patch("main.UserService")
@patch("main.UserDTO")
@patch("main.logger")
@pytest.mark.asyncio()
async def test_user_service_add_ok(
        mock_logger,
        mock_user_dto_class,
        mock_user_service_class,
        mock_get_async_session,
):
    """
    Checking whether the add method returns expected
    result in a successful case.
    """
    mock_name = Mock()
    mock_async_engine = Mock()

    mock_user_service_class.return_value = AsyncMock()

    result = await user_service_add(name=mock_name, async_engine=mock_async_engine)  # noqa

    mock_get_async_session.assert_awaited_once_with(mock_async_engine)
    mock_user_service_class.assert_called_once_with(mock_get_async_session.return_value)  # noqa
    mock_user_dto_class.assert_called_once_with(name=mock_name)
    mock_user_service_class.return_value.add.assert_awaited_once_with(
        mock_user_dto_class.return_value,
    )

    # check if the logger.debug in "try" block was called
    mock_logger.debug.assert_called_once()
    # check if the logger didn't raise an error in "except" block
    mock_logger.error.assert_not_called()

    assert result is None


@patch("main.get_async_session")
@patch("main.UserService")
@patch("main.UserDTO")
@patch("main.logger")
@pytest.mark.asyncio()
async def test_user_service_add_validation_error(
        mock_logger,
        mock_user_dto_class,
        mock_user_service_class,
        mock_get_async_session,
):
    """
    Checking if the add method raises ValidationError
    if we add name attribute as an integer or the
    given string is longer than it's allowed.
    """
    mock_name = Mock()
    mock_async_engine = Mock()

    mock_user_service_class.return_value = AsyncMock()

    mock_add = AsyncMock()
    mock_add.side_effect = ValidationError.from_exception_data(
        title="ValidationError",
        line_errors=[],
    )

    mock_user_service_class.return_value.add = mock_add

    result = await user_service_add(name=mock_name, async_engine=mock_async_engine)  # noqa

    mock_get_async_session.assert_awaited_once_with(mock_async_engine)
    mock_user_service_class.assert_called_once_with(mock_get_async_session.return_value)  # noqa
    mock_add.assert_awaited_once_with(
        mock_user_dto_class.return_value,
    )

    mock_logger.debug.assert_not_called()
    mock_logger.error.assert_called_once()

    assert result is None


@patch("main.get_async_session")
@patch("main.UserService")
@patch("main.logger")
@pytest.mark.asyncio()
async def test_user_service_get_ok(
        mock_logger,
        mock_user_service_class,
        mock_get_async_session,
):
    """
    Checking whether the get method returns expected
    result in a successful case.
    """
    mock_pk = Mock()
    mock_async_engine = Mock()

    mock_user_service_class.return_value = AsyncMock()

    result = await user_service_get(pk=mock_pk, async_engine=mock_async_engine)

    mock_get_async_session.assert_awaited_once_with(mock_async_engine)
    mock_user_service_class.assert_called_once_with(mock_get_async_session.return_value)  # noqa
    mock_user_service_class.return_value.get.assert_awaited_once_with(pk=mock_pk)

    mock_logger.debug.assert_called_once()
    mock_logger.error.assert_not_called()

    assert result is None


@patch("main.get_async_session")
@patch("main.UserService")
@patch("main.logger")
@pytest.mark.asyncio()
async def test_user_service_get_validation_error(
        mock_logger,
        mock_user_service_class,
        mock_get_async_session,
):
    """
    Checking if the get method raises ValidationError
    if we request a non-existent user.
    """
    mock_pk = Mock()
    mock_async_engine = Mock()

    mock_get = AsyncMock()
    mock_get.side_effect = ValidationError.from_exception_data(
        title="ValidationError",
        line_errors=[],
    )
    mock_user_service_class.return_value.get = mock_get

    result = await user_service_get(pk=mock_pk, async_engine=mock_async_engine)

    mock_get_async_session.assert_awaited_once_with(mock_async_engine)
    mock_user_service_class.assert_called_once_with(mock_get_async_session.return_value)  # noqa
    mock_get.assert_called_once_with(pk=mock_pk)

    mock_logger.debug.assert_not_called()
    mock_logger.error.assert_called_once()

    assert result is None


@patch("main.get_async_session")
@patch("main.UserService")
@patch("main.logger")
@pytest.mark.asyncio()
async def test_user_service_get_data_error(
        mock_logger,
        mock_user_service_class,
        mock_get_async_session,
):
    """
    Checking if the get method raises DataError
    if we request a user with a string instead of an integer.
    """
    mock_pk = Mock()
    mock_async_engine = Mock()

    mock_get = AsyncMock()
    mock_get.side_effect = DataError()

    mock_user_service_class.return_value.get = mock_get

    result = await user_service_get(pk=mock_pk, async_engine=mock_async_engine)

    mock_get_async_session.assert_awaited_once_with(mock_async_engine)
    mock_user_service_class.assert_called_once_with(mock_get_async_session.return_value)  # noqa
    mock_get.assert_called_once_with(pk=mock_pk)

    mock_logger.debug.assert_not_called()
    mock_logger.error.assert_called_once()

    assert result is None


@patch("main.get_async_session")
@patch("main.UserService")
@patch("main.logger")
@pytest.mark.asyncio()
async def test_user_service_get_db_api_error(
        mock_logger,
        mock_user_service_class,
        mock_get_async_session,
):
    """
    Checking if the get method raises DBAPIError
    if we request a user without passing a primary key.
    """
    mock_pk = Mock()
    mock_async_engine = Mock()

    mock_get = AsyncMock()
    mock_get.side_effect = DBAPIError(statement="db_api_error", params=[], orig=BaseException())  # noqa

    mock_user_service_class.return_value.get = mock_get

    result = await user_service_get(pk=mock_pk, async_engine=mock_async_engine)

    mock_get_async_session.assert_awaited_once_with(mock_async_engine)
    mock_user_service_class.assert_called_once_with(mock_get_async_session.return_value)  # noqa
    mock_get.assert_called_once_with(pk=mock_pk)

    mock_logger.debug.assert_not_called()
    mock_logger.error.assert_called_once()

    assert result is None
