from unittest.mock import AsyncMock, MagicMock, Mock, patch

import pydantic
import pytest
from sqlalchemy.exc import DBAPIError

from services.user import UserService


@patch("services.user.User")
@patch("services.user.UserDTO")
@pytest.mark.asyncio()
async def test_userservice_add_ok(mock_user_dto_class, mock_user):
    """
    Checking whether the add method returns expected
    result in a successful case.
    """
    mock_async_session = MagicMock()

    mock_async_session.return_value.__aenter__.return_value.add = Mock()

    mock_user_dto = Mock()
    mock_user_dto.name = "TestTest"

    user_service = UserService(mock_async_session)
    result = await user_service.add(mock_user_dto)

    mock_async_session.return_value.__aenter__.assert_awaited_once()

    mock_async_session.return_value.__aenter__.return_value.add.assert_called_once_with(  # noqa
        mock_user.return_value,
    )
    mock_async_session.return_value.__aenter__.return_value.commit.assert_awaited_once()  # noqa
    mock_async_session.return_value.__aenter__.return_value.refresh.assert_awaited_once_with(  # noqa
        mock_user.return_value,
    )
    mock_user_dto_class.model_validate.assert_called_once_with(mock_user.return_value)  # noqa

    mock_async_session.return_value.__aexit__.assert_awaited_once()
    assert result == mock_user_dto_class.model_validate.return_value


@pytest.mark.asyncio()
async def test_userservice_add_attribute_error_invalid_data():
    """
    Checking if the add method raises AttributeError
    with invalid data passed as a name attribute.
    """
    mock_async_session = MagicMock()
    user_service = UserService(mock_async_session)
    with pytest.raises(AttributeError):
        await user_service.add(123)


@pytest.mark.asyncio()
async def test_userservice_add_type_error_invalid_data():
    """
    Checking if the add method raises TypeError
    with no data passed as a name attribute.
    """
    mock_async_session = MagicMock()
    user_service = UserService(mock_async_session)
    with pytest.raises(TypeError):
        await user_service.add()


@patch("services.user.User")
@patch("services.user.UserDTO")
@pytest.mark.asyncio()
async def test_userservice_get_ok(mock_user_dto_class, mock_user):
    """
    Checking whether the get method returns expected
    result in a successful case.
    """
    mock_async_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value.get = AsyncMock()

    mock_pk = 1

    user_service = UserService(mock_async_session)
    result = await user_service.get(mock_pk)

    mock_async_session.return_value.__aenter__.assert_awaited_once()

    mock_async_session.return_value.__aenter__.return_value.get.assert_awaited_once_with(  # noqa
        mock_user,
        mock_pk,
    )
    mock_user_dto_class.model_validate.assert_called_once_with(
        mock_async_session.return_value.__aenter__.return_value.get.return_value,
    )

    mock_async_session.return_value.__aexit__.assert_awaited_once()

    assert result == mock_user_dto_class.model_validate.return_value


@pytest.mark.asyncio()
async def test_userservice_get_validation_error_no_such_user():
    """
    Checking if the get method raises ValidationError
    if we request a non-existent user.
    """
    mock_async_session = MagicMock()
    user_service = UserService(mock_async_session)
    with pytest.raises(pydantic.ValidationError):
        await user_service.get(1)


@pytest.mark.asyncio()
async def test_userservice_get_dbapi_error_invalid_data():
    """
    Checking if the get method raises DBAPIError
    if we request user with a string instead of integer.
    """
    mock_async_session = MagicMock()
    mock_async_session.return_value.__aenter__.return_value.get.side_effect = DBAPIError(  # noqa
        statement="",
        params=[],
        orig=Exception(),
    )
    user_service = UserService(mock_async_session)
    with pytest.raises(DBAPIError):
        await user_service.get("string")
