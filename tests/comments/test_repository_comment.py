from datetime import datetime

import unittest
from unittest.mock import MagicMock
from sqlalchemy.orm import Session

from src.database.models import Comment, User
from src.schemas import CommentModel
from src.repository.comments import (
    create_comment,
    get_comments,
    get_comment,
    get_user_by_comment_id,
    delete_comments,
    edit_comments

)


class TestComment(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock(spec=Session)
        self.current_user = User(id=123)
        self.post = MagicMock()
        self.post.id = 1

    def tearDown(self):
        # Roll back the session to clear the database after each test
        self.db.rollback()

    async def test_create_comment_successful(self):
        body = CommentModel(comment_text="Hello, world!")
        result = await create_comment(body, self.post.id, self.db, self.current_user)

        self.assertIsInstance(result, Comment)
        self.assertEqual(result.comment_text, body.comment_text)
        self.assertEqual(result.post_id, self.post.id)
        self.assertEqual(result.user_id, self.current_user.id)

    async def test_create_comment_invalid_post_id(self):
        body = CommentModel(comment_text="Hello, world!")
        self.db.query.return_value.filter_by.return_value.first.return_value = None

        result = await create_comment(body, 999, self.db, self.current_user)

        self.assertIsNone(result)
        self.db.query.return_value.filter_by.assert_called_once_with(id=999)

    async def test_get_comments_successful(self):
        skip = 0
        limit = 10
        comments = [Comment(), Comment(), Comment()]
        self.db.query().filter_by().offset(skip).limit(limit).all = comments

        result = await get_comments(skip, limit, self.db, self.post.id)

        self.assertEqual(result, comments)
        self.db.query.return_value.filter_by.assert_called_once_with(post_id=self.post.id)
        self.db.query.return_value.filter_by.return_value.offset.assert_called_once_with(skip)
        self.db.query.return_value.filter_by.return_value.offset.return_value.limit.assert_called_once_with(limit)
        self.db.query.return_value.filter_by.return_value.offset.return_value.limit.return_value.all.assert_called_once()

    async def test_get_user_by_comment_id_successful(self):
        user = User(id=1)

        result = await get_user_by_comment_id(self.db, user.id)

        self.assertEqual(result, user.id)
        self.db.query.return_value.filter_by.assert_called_once_with(id=user.id)
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()

    async def test_get_user_by_comment_id_none(self):
        user = User(id=3232323)

        self.db.query.return_value.filter_by.return_value.first.return_value = None

        result = get_user_by_comment_id(self.db, user.id)

        self.assertIsNone(result)
        self.db.query.return_value.filter_by.assert_called_once_with(id=user.id)
        self.db.query.return_value.filter_by.return_value.first.assert_called_once()

    async def test_get_comment(self):
        # create a mock database session and comment object
        comment = Comment(id=1, comment_text='test comment', post_id=1, user_id=1)

        # mock the query method to return the comment object
        self.db.query().filter_by().first.return_value = comment

        # call the get_comment function and assert that it returns the comment object
        assert get_comment(self.db, 1) == comment

        # assert that the query method was called with the correct arguments
        self.db.query.assert_called_once_with(Comment)
        self.db.query().filter_by.assert_called_once_with(id=1)
        self.db.query().filter_by().first.assert_called_once()

    async def test_delete_comments(self):
        comment = Comment()

        self.db.query().filter_by().first.return_value = comment

        # Create a mock User object for testing
        user = User(id=1)

        # Call the function with the mock arguments
        await delete_comments(1, user, self.db)

        # Check that the comment was deleted and committed to the database
        assert self.db.delete.called_with(comment)
        assert self.db.commit.called

    async def test_edit_comments_wrong_user(self):
        comment = Comment(id=1)
        # Create a CommentModel instance with the new comment text
        new_comment_text = "Updated comment text"
        comment_model = CommentModel(comment_text=new_comment_text)

        # Create a different user to try to edit the comment
        user2 = User(name="Jane Doe", email="janedoe@example.com", password="password")
        self.db.add(user2)
        self.db.commit()

        # Call the edit_comments function with the comment_id, CommentModel instance, database session, and current user
        edited_comment = await edit_comments(comment_id=comment.id, body=comment_model, db=self.db,
                                             current_user=user2)

        # Check that the edited_comment is None, since user2 is not authorized to edit the comment
        self.assertIsNone(edited_comment)

    async def test_edit_comments_invalid_comment_id(self):
        # Create a CommentModel instance with the new comment text
        new_comment_text = "Updated comment text"
        comment_model = CommentModel(comment_text=new_comment_text)

        edited_comment = await edit_comments(comment_id=-1, body=comment_model, db=self.db,
                                             current_user=self.current_user)

        # Check that the edited_comment is None, since no comment with that id exists in the database
        self.assertIsNone(edited_comment)

    async def test_edit_comments(self):
        comment = Comment(id=1)
        # Create a CommentModel instance with the new comment text
        new_comment_text = "Updated comment text"
        comment_model = CommentModel(comment_text=new_comment_text)

        # Call the edit_comments function with the comment_id, CommentModel instance, database session, and current user
        edited_comment = await edit_comments(comment_id=comment.id, body=comment_model, db=self.db,
                                             current_user=self.current_user)

        # Check that the edited_comment is not None and has the correct comment_text and updated_at values
        self.assertIsNotNone(edited_comment)
        self.assertEqual(edited_comment.comment_text, new_comment_text)
        self.assertLessEqual(edited_comment.updated_at, datetime.now())


if __name__ == '__main__':
    unittest.main()
