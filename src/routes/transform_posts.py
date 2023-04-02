import io
import base64
from typing import List
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session
import cloudinary
import qrcode
import qrcode.image.svg
import qrcode.image.base

from src.schemas_transform_posts import TransformImageModel, URLTransformImageResponse, SaveTransformImageModel, \
    TransformImageResponse
from src.database.connect import get_db
from src.database.models import User
from src.services.transform_posts import create_list_transformation
import src.repository.transform_posts as rep_transform
from src.services.messages_templates import NOT_FOUND
from src.services.auth import auth_service


router = APIRouter(prefix='/image/transform', tags=['Transform Image'])


@router.get('/user', response_model=List[TransformImageResponse], status_code=status.HTTP_200_OK)
async def get_list_of_transformed_for_user(current_user: User = Depends(auth_service.get_current_user),
                                           db: Session = Depends(get_db)):
    """
    The get_list_of_transformed_for_user function returns a list of all the transformed images for a given user.
        The function takes in an optional current_user parameter, which is the currently logged-in user.
        If no current_user is provided, then it will default to None.

    :param current_user: User: Get the user who is currently logged in
    :param db: Session: Get the database session
    :return: A list of all transformed images for the current user
    """
    return await rep_transform.get_all_transform_images_for_user(current_user, db)



@router.post('/{base_image_id}', response_model=URLTransformImageResponse, status_code=status.HTTP_200_OK)
async def transformation_for_image(base_image_id: int, body: TransformImageModel,
                                   current_user: User = Depends(
                                       auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    """
    The transformation_for_image function takes in a base_image_id, body, current_user and db.
    The function then calls the get_image_for transform method from the repos/transformations.py file to retrieve an image url for transformation.
    If no image is found with that id, it raises a 404 error message saying &quot;Image not found&quot;.
    Otherwise it configures cloudinary using my api key and secret key (which I have hidden).
    It then creates a list of transformations based on what was passed into the body of this request (the user's desired transformations).
    Finally it builds an url for that

    :param base_image_id: int: Get the image from the database
    :param body: TransformImageModel: Get the transformation parameters from the request body
    :param current_user: User: Get the current user from the database
    :param db: Session: Get a database session
    :return: A url of the transformed image
    """
    image_url = await rep_transform.get_image_for_transform(base_image_id, current_user, db)
    if image_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    cloudinary.config(
        cloud_name='drilpksk7',
        api_key='326193329941471',
        api_secret='1YqMfm4NEIJApzklq_lEaolH7-I',
        secure=True
    )
    transform_list = create_list_transformation(body)
    url = cloudinary.CloudinaryImage(image_url).build_url(
        transformation=transform_list)
    return {'url': url}


@router.post('/save/{base_image_id}', response_model=TransformImageResponse, status_code=status.HTTP_201_CREATED)
async def save_transform_image(base_image_id: int, body: SaveTransformImageModel,
                               current_user: User = Depends(
                                   auth_service.get_current_user),
                               db: Session = Depends(get_db)):
    """
    The save_transform_image function is used to save a transformed image.
        The function takes in the base_image_id, body, current user and database as parameters.
        It then calls the set_transform_image function from rep transform which saves the transformed image into
        the database and returns it if successful or None otherwise.

    :param base_image_id: int: Specify the id of the image that is being transformed
    :param body: SaveTransformImageModel: Pass the url of the image to be saved
    :param current_user: User: Get the current user
    :param db: Session: Get the database session
    :return: The image with the specified id
    """
    img = await rep_transform.set_transform_image(base_image_id, body.url, current_user, db)
    if img is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return img


@router.get('/qrcode/{transform_image_id}', status_code=status.HTTP_200_OK)
async def get_qrcode_for_transform_image(transform_image_id: int, current_user: User = Depends(auth_service.get_current_user),
                                         db: Session = Depends(get_db)):
    """
    The get_qrcode_for_transform_image function is used to generate a QR code for the transform image.
    The function takes in an integer representing the id of the transform image and returns a string containing
    the base64 encoded QR code.

    :param transform_image_id: int: Get the image_url from the database
    :param current_user: User: Get the current user
    :param db: Session: Access the database
    :return: A base64 encoded qr code
    """
    image_url = await rep_transform.get_transform_image(transform_image_id, current_user, db)
    if image_url is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    qr = qrcode.make(image_url.photo_url)
    buf = io.BytesIO()
    qr.save(buf)
    qr_code = base64.b64encode(buf.getvalue()).decode('ascii')
    return qr_code


@router.get('/{transform_image_id}', response_model=TransformImageResponse, status_code=status.HTTP_200_OK)
async def get_transformed_image(transform_image_id: int, current_user: User = Depends(auth_service.get_current_user),
                                db: Session = Depends(get_db)):
    """
    The get_transformed_image function returns a transformed image.
        The function takes in the transform_image_id and current user as parameters.
        It then calls the get_transform_image function from repos/transformations to retrieve the transformed image.
        If no such image is found, it raises an HTTPException with status code 404 and detail NOT FOUND.

    :param transform_image_id: int: Get the image id from the url
    :param current_user: User: Get the current user from the auth_service
    :param db: Session: Pass the database session to the function
    :return: A transformed image
    """
    img = await rep_transform.get_transform_image(transform_image_id, current_user, db)
    if img is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)
    return img


@router.delete('/{transform_image_id}', status_code=status.HTTP_204_NO_CONTENT)
async def remove_transformed_image(transform_image_id: int, current_user: User = Depends(auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    """
    The remove_transformed_image function is used to remove a transformed image from the database.
        The function takes in an integer representing the id of the transform_image object that will be removed,
        and returns a JSON response containing information about whether or not it was successful.

    :param transform_image_id: int: Identify the image that is to be removed
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Pass the database session to the repository
    :return: An image object
    """
    img = await rep_transform.remove_transform_image(transform_image_id, current_user, db)
    if img is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=NOT_FOUND)


@router.get('/all/{base_image_id}', response_model=List[TransformImageResponse], status_code=status.HTTP_200_OK)
async def get_list_of_transformed_for_image(base_image_id: int,
                                            current_user: User = Depends(auth_service.get_current_user),
                                            db: Session = Depends(get_db)):
    """
    The get_list_of_transformed_for_image function returns a list of all transformed images for the given base image.
        The function takes in an integer representing the id of the base image and returns a list of dictionaries, each
        dictionary containing information about one transformed image.

    :param base_image_id: int: Get the base image id from the url
    :param current_user: User: Get the user that is currently logged in
    :param db: Session: Access the database
    :return: A list of transformed images for the base image id
    """
    return await rep_transform.get_all_transform_images(base_image_id, current_user, db)


