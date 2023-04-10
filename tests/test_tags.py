import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Tag
from src.repository.tags import get_tag_by_name, create_tag, get_tags_list
from src.schemas import TagCreate, TagBase


class TestPostCRUD(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user_mock = User(id=1)
