import unittest
from unittest.mock import Mock
from sqlalchemy.orm import Session

from src.database.models import User, UserRole
from src.repository.users import banned_user
from src.services.messages_templates import PERMISSION_ERROR


class TestBannedUser(unittest.TestCase):
    async def test_banned_user_success(self):
        session_mock = Mock(spec=Session)
        user_mock = Mock(spec=User)
        user_mock.user_role = UserRole.Admin.name
        result = await banned_user(123, user_mock, session_mock)
        self.assertEqual(result.is_active, False)
        session_mock.commit.assert_called_once()

    async def test_banned_user_permission_error(self):
        session_mock = Mock(spec=Session)
        user_mock = Mock(spec=User)
        user_mock.user_role = UserRole.User.name
        result = await banned_user(123, user_mock, session_mock)
        self.assertEqual(result, PERMISSION_ERROR)
