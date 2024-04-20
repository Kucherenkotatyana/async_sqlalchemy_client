from unittest.mock import Mock

from dto.user import UserDTO


def test_user_dto_ok():
    """
    Check if the UserDTO class validates data in a proper way.
    """
    user = UserDTO(pk=1, name="TestName")
    assert user.pk == 1
    assert user.name == "TestName"


def test_user_dto_no_pk():
    """
    UserDTO class returns None for primary key.
    """
    user = UserDTO(name="TestName")
    assert user.name == "TestName"
    assert user.pk is None


def test_user_dto_from_attributes_ok():
    """
    Check if UserDTO class creates its instances using
    attributes of the given object.
    """
    user_mock = Mock()
    user_mock.pk = 1
    user_mock.name = "TestName"

    user_dto = UserDTO.model_validate(user_mock)

    assert user_dto.pk == user_mock.pk
    assert user_dto.name == user_mock.name
