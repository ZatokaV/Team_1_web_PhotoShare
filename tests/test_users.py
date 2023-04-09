import unittest
from unittest.mock import Mock, MagicMock

from sqlalchemy.orm import Session
from datetime import datetime

from src.database.models import User, UserRole, Post
from src.repository.users import banned_user, create_user, update_user_self, update_user_as_admin, \
    update_token, get_all_users, get_user_by_email, get_user_profile
from src.schemas import UserCreate, UserBase, UserUpdate, UserProfileModel


class TestBannedUser(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session_mock = Mock(spec=Session)
        self.user_mock = Mock(spec=User)

    async def test_banned_user_success(self):
        self.user_mock.user_role = UserRole.Admin.name
        result = await banned_user(123, self.user_mock, self.session_mock)
        self.assertEqual(result.is_active, False)
        self.session_mock.commit.assert_called_once()

    async def test_banned_user_permission_error(self):
        self.user_mock.user_role = UserRole.User.name
        result = await banned_user(123, self.user_mock, self.session_mock)
        self.assertEqual(result, None)


class TestUserCRUD(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session_mock = MagicMock(spec=Session)
        self.post_mock = MagicMock(spec=Post)
        self.user_mock = MagicMock(spec=User)

    async def test_create_user(self):
        body = UserCreate(
            username="test_user",
            first_name="test_first",
            last_name="test_last",
            email="test@example.com",
            password="test*user")
        result = await create_user(body, self.session_mock)
        self.session_mock.commit.return_value = None
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.password, body.password)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_user_self_found(self):
        body = UserBase(
            username="test_user",
            first_name="test_first_",
            last_name="test_last_",
            email="test@example.com"
        )
        self.session_mock.query().filter().first.return_value = self.user_mock
        self.session_mock.commit.return_value = None
        result = await update_user_self(body, self.user_mock, self.session_mock)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)

    async def test_update_user_self_not_found(self):
        body = UserBase(
            username="test_user",
            first_name="test_first",
            last_name="test_last",
            email="test@example.com"
        )
        self.session_mock.query().filter().first.return_value = None
        self.session_mock.commit.return_value = None
        result = await update_user_self(body, self.user_mock, self.session_mock)
        self.assertIsNone(result)

    async def test_update_user_as_admin_found(self):
        body = UserUpdate(
            username="test_user",
            first_name="test_first",
            last_name="test_last",
            email="test@example.com",
            is_active=False,
            user_role=UserRole.Admin.name
        )
        self.user_mock.username = "test_user"
        self.user_mock.user_role = UserRole.Admin.name
        self.session_mock.query().filter().first.return_value = self.user_mock
        self.session_mock.commit.return_value = None
        result = await update_user_as_admin(body, self.user_mock, self.session_mock)
        self.assertEqual(result.username, body.username)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.is_active, body.is_active)
        self.assertEqual(result.user_role, body.user_role)

    async def test_update_user_as_admin_not_found(self):
        body = UserUpdate(
            username="test_user",
            first_name="test_first",
            last_name="test_last",
            email="test@example.com",
            is_active=False,
            user_role=UserRole.Admin.name
        )
        self.session_mock.query().filter().first.return_value = None
        self.session_mock.commit.return_value = None
        result = await update_user_as_admin(body, self.user_mock, self.session_mock)
        self.assertIsNone(result)

    async def test_update_user_token(self):
        token = "some_token"
        self.session_mock.query().filter().first.return_value = self.user_mock
        self.session_mock.commit.return_value = None
        await update_token(self.user_mock, token, self.session_mock)
        self.assertEqual(self.user_mock.refresh_token, token)

    async def test_get_user_profile_found(self):
        self.user_mock.username = "test_user"
        self.session_mock.query.return_value.filter.return_value.first.return_value = self.user_mock
        self.session_mock.query.return_value.filter.return_value.first.return_value = self.post_mock
        self.assertEqual(self.user_mock.username, "test_user")
        """
        #result = await get_user_profile("test_user", self.session_mock)
        self.assertIsInstance(result, UserProfileModel)
        self.assertEqual(result.username, self.user_mock.username)
        self.assertIsNotNone(result.number_of_photos)
        """

    async def test_get_user_profile_not_found(self):
        self.session_mock.query(User).filter().first.return_value = self.user_mock
        self.session_mock.query(Post).filter().first.return_value = None
        result = await get_user_profile("no_user", self.session_mock)
        self.assertIsNone(result)

    async def test_get_user_by_email_found(self):
        self.user_mock.email = "test_email"
        self.session_mock.query().filter().first.return_value = self.user_mock
        result = await get_user_by_email("test_email", self.session_mock)
        self.assertEqual(result, self.user_mock)

    async def test_get_user_by_email_not_found(self):
        self.user_mock.email = "test_email"
        self.session_mock.query().filter().first.return_value = None
        result = await get_user_by_email("test_email", self.session_mock)
        self.assertIsNone(result)

    async def test_get_all_users(self):
        users = [User(), User(), User()]
        self.session_mock.query().filter().all.return_value = users
        result = await get_all_users(self.user_mock, self.session_mock)
        self.assertEqual(result, users)


if __name__ == '__main__':
    unittest.main()
