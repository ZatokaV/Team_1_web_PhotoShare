from typing import List

from sqlalchemy import and_
from sqlalchemy.orm import Session

from src.database.models import TransformPosts, Post, User, UserRole


async def get_image_for_transform(image_id: int, current_user: User, db: Session) -> str | None:
    """
    The get_image_for_transform function is used to retrieve the image path for a given image id.
        The function takes in an integer representing the id of the desired image, a User object representing
        the current user, and a Session object that represents our database connection.  If we are able to find
        an image with this ID in our database (and if we are not admin), then we return its photo_url attribute.

    :param image_id: int: Get the image from the database
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: The path to the image that will be transformed
    """
    if current_user.user_role == UserRole.Admin.name:
        image = db.query(Post).filter(Post.id == image_id).first()
    else:
        image = db.query(Post).filter(and_(Post.id == image_id, Post.user_id == current_user.id)).first()
    image_path = None
    if image:
        image_path = image.photo_url
    return image_path


async def set_transform_image(image_id: int, modify_url: str, current_user: User, db: Session) -> TransformPosts | None:
    """
    The set_transform_image function takes in an image_id, modify_url, current_user and db.
        If the user is an admin or if the user owns the photo then it will create a new TransformPosts object with
        photo url and id. It will add this to the database and commit it.

    :param image_id: int: Identify the image that will be modified
    :param modify_url: str: Store the url of the modified image
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: A transform posts object or none
    """
    image = None
    if current_user.user_role == UserRole.Admin.name:
        photo = db.query(Post).filter(Post.id == image_id).first()
    else:
        photo = db.query(Post).filter(and_(Post.id == image_id, Post.user_id == current_user.id)).first()
    if photo:
        image = TransformPosts(photo_url=modify_url, photo_id=photo.id)
        db.add(image)
        db.commit()
        db.refresh(image)
    return image


async def get_transform_image(image_id: int, current_user: User, db: Session) -> TransformPosts | None:
    """
    The get_transform_image function is used to retrieve a single image from the database.
        The function takes in an image_id, current_user and db as parameters.
        If the user is an admin, then it will return all images with that id.
        Otherwise, it will only return images with that id if they were created by the current user.

    :param image_id: int: Get the image id from the database
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: An image from the database
    """
    if current_user.user_role == UserRole.Admin.name:
        img = db.query(TransformPosts).filter(TransformPosts.id == image_id).first()
    else:
        img = db.query(TransformPosts).join(Post).filter(and_(TransformPosts.id == image_id,
                                                              Post.user_id == current_user.id)).first()
    return img


async def remove_transform_image(image_id: int, current_user: User, db: Session) -> TransformPosts | None:
    """
    The remove_transform_image function is used to remove a transform image from the database.
        The function takes in an image_id and current_user as parameters, and returns the removed TransformPosts object.
        If no such TransformPosts object exists, None is returned instead.

    :param image_id: int: Specify the image id of the image that is to be removed
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: The image that was removed, or none if it failed
    :doc-author: Trelent
    """
    if current_user.user_role == UserRole.Admin.name:
        img = db.query(TransformPosts).filter(TransformPosts.id == image_id).first()
    else:
        img = db.query(TransformPosts).join(Post).filter(and_(Post.id == image_id,
                                                              Post.user_id == current_user.id)).first()
    if img:
        db.delete(img)
        db.commit()
    return img


async def get_all_transform_images(image_id: int, current_user: User, db: Session) -> List[TransformPosts]:
    """
    The get_all_transform_images function returns a list of all transform images for the given image id.
        If the current user is an admin, then it will return all transform images for that image id.
        Otherwise, it will only return those transform images that belong to the current user.

    :param image_id: int: Filter the transform posts table by photo_id
    :param current_user: User: Check if the user is an admin or not
    :param db: Session: Access the database
    :return: A list of all the images that are transformed from an image
    :doc-author: Trelent
    """
    if current_user.user_role == UserRole.Admin.name:
        list_image = db.query(TransformPosts).filter(TransformPosts.photo_id == image_id).all()
    else:
        list_image = db.query(TransformPosts).join(Post).filter(and_(Post.id == image_id,
                                                                     Post.user_id == current_user.id)).all()
    return list_image


async def get_all_transform_images_for_user(current_user: User, db: Session) -> List[TransformPosts]:
    if current_user.user_role == UserRole.Admin.name:
        list_image = db.query(TransformPosts).all()
    else:
        list_image = db.query(TransformPosts).join(Post).filter(Post.user_id == current_user.id).all()
    return list_image
