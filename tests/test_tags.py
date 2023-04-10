import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Tag
from src.repository.tags import get_tag_by_name, create_tag, get_tags_list
from src.schemas import TagCreate, TagBase


class TestTag(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user_mock = User(id=1)

    async def test_get_tag_by_name(self):

        tag_name = "test"
        tag = Tag(
            id=0,
            tag=tag_name
        )

        self.session.query(Tag).filter().first.return_value = tag
        result = get_tag_by_name(tag_name=tag_name, db=self.session)
        self.assertEqual(result.tag, tag_name)

    async def test_get_tag_by_name_not_found(self):
        self.session.query(Tag).filter().first.return_value = None
        result = get_tag_by_name(tag_name="", db=self.session)
        self.assertIsNone(result)

    async def test_create_tag(self):
        tag_name = "test"
        result = create_tag(tag_name=tag_name, user=self.user_mock, db=self.session)
        self.assertEqual(tag_name, result.tag)
        self.assertTrue(hasattr(result, "id"))

    async def test_get_tags_list(self):
        tag_name = "test"
        tags = [tag_name]
        tag = Tag(
            id=0,
            tag=tag_name
        )

        self.session.query(Tag).filter().first.return_value = tag

        result = get_tags_list(tags=tags, user=self.user_mock, db=self.session)
        self.assertEqual(len(result), 1)
        self.assertEqual(tag_name, result[0].tag)


if __name__ == '__main__':
    unittest.main()
