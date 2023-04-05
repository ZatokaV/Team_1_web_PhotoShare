import unittest
from unittest.mock import Mock

from sqlalchemy.orm import Session

from src.database.models import User, UserRole
from src.repository.users import banned_user, create_user, update_user_self, update_user_as_admin, \
    update_token, get_all_users, get_user_by_email, get_user_profile
from src.schemas import UserCreate
from src.services.auth import auth_service


class TestBannedUser(unittest.TestCase):
    def setUp(self) -> None:
        self.session_mock = Mock(spec=Session)
        self.user_mock = Mock(spec=User)

    async def test_banned_user_success(self):
        #session_mock = Mock(spec=Session)
        #user_mock = Mock(spec=User)
        self.user_mock.user_role = UserRole.Admin.name
        result = await banned_user(123, self.user_mock, self.session_mock)
        self.assertEqual(result.is_active, False)
        self.session_mock.commit.assert_called_once()

    async def test_banned_user_permission_error(self):
        #session_mock = Mock(spec=Session)
        #user_mock = Mock(spec=User)
        self.user_mock.user_role = UserRole.User.name
        result = await banned_user(123, self.user_mock, self.session_mock)
        self.assertEqual(result, None)


class TestUserCRUD(unittest.TestCase):
    def setUp(self) -> None:
        self.session_mock = Mock(spec=Session)
        self.user_mock = Mock(spec=User)

    async def test_create_user(self):
        body = UserCreate(
            username="test_user",
            first_name="test_first",
            last_name="test_last",
            email="test@example.com",
            password="test*user")
        result = await create_user(body, self.session_mock)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(
            result.password, auth_service.get_password_hash(body.password))
        self.assertEqual(result.user_role, UserRole.User.name)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_user_self_found(self):
        pass

    async def test_update_user_self_not_found(self):
        pass

    async def test_update_user_as_admin_found(self):
        pass

    async def test_update_user_as_admin_found(self):
        pass

    async def test_update_user_token(self):
        pass

    async def test_get_user_profile_found(self):
        pass

    async def test_get_user_profile_not_found(self):
        pass

    async def test_get_user_by_email_found(self):
        pass

    async def test_get_user_by_email_not_found(self):
        pass

    async def test_get_all_users(self):
        pass


if __name__ == '__main__':
    unittest.main()
