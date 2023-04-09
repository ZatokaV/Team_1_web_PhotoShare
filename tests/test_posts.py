import unittest
from unittest.mock import MagicMock

from sqlalchemy.orm import Session

from src.database.models import User, Post
from src.repository.posts import create_post, get_post, get_user_posts, update_post, remove_post, change_post_mark
from src.schemas import PostCreate


class TestPostCRUD(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user_mock = User(id=1)

    async def test_create_post(self):
        body = PostCreate(
            description="Test description",
            tags=["first", "second", "third"]
        )
        file_path = "test_path"

        result = await create_post(body, file_path, self.session, self.user_mock)

        self.assertEqual(result.description, body.description)
        self.assertEqual(result.photo_url, file_path)
        self.assertEqual(result.user_id, self.user_mock.id)
        self.assertEqual(len(result.tags), len(body.tags))
        # self.assertEqual(result.tags[0].tag, body.tags[0])
        # self.assertEqual(result.tags[1].tag, body.tags[1])
        # self.assertEqual(result.tags[2].tag, body.tags[2])
        self.assertTrue(hasattr(result, "id"))

    async def test_get_post(self):
        post_id = 1
        post = Post(
            id=post_id,
            description="Test description",
            photo_url="test_path"
        )

        self.session.query().filter().first.return_value = post

        result = await get_post(post_id=post_id, db=self.session)

        self.assertEqual(result.id, post.id)
        self.assertEqual(result.description, post.description)
        self.assertEqual(result.photo_url, post.photo_url)

    async def test_get_post_not_found(self):

        self.session.query(Post).filter().first.return_value = None

        result = await get_post(post_id=0, db=self.session)
        self.assertIsNone(result)

    async def test_get_user_posts(self):
        return_value = [Post(), Post(), Post()]
        self.session.query(Post).filter().all.return_value = return_value
        result = await get_user_posts(user_id=0, db=self.session)

        self.assertEqual(return_value, result)

    async def test_update_post(self):
        post_id = 0
        return_value = Post(
            id=post_id,
            description="Test description",
            photo_url="test_path",
            tags=[]
        )

        self.session.query().filter().first.return_value = return_value

        body = PostCreate(
            description="Update description",
            tags=[]
        )

        result = await update_post(post_id=post_id, body=body, db=self.session, user=self.user_mock)
        self.assertEqual(result.id, post_id)
        self.assertEqual(result.description, body.description)

    async def test_update_post_not_found(self):
        self.session.query().filter().first.return_value = None

        body = PostCreate(
            description="Update description",
            tags=[]
        )
        self.session.query(Post).filter().first.return_value = None

        result = await update_post(post_id=0, body=body, db=self.session, user=self.user_mock)
        self.assertIsNone(result)


    async def test_remove_post(self):
        post_id = 1
        post = Post(
            id=post_id,
            description="Test description",
            photo_url="test_path"
        )

        self.session.query().filter().first.return_value = post

        result = await remove_post(post_id=post_id, db=self.session)

        self.assertEqual(post, result)

    async def test_remove_post_not_found(self):
        self.session.query().filter().first.return_value = None

        result = await remove_post(post_id=1, db=self.session)

        self.assertIsNone(result)

    async def test_change_post_mark(self):
        post_id = 1
        marked = False
        post = Post(
            id=post_id,
            description="Test description",
            photo_url="test_path",
            marked=marked
        )

        self.session.query().filter().first.return_value = post

        result = await change_post_mark(post_id=post_id, db=self.session)

        self.assertEqual(marked, not result.marked)

    async def test_change_post_mark_not_found(self):
        self.session.query().filter().first.return_value = None

        result = await change_post_mark(post_id=1, db=self.session)

        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
