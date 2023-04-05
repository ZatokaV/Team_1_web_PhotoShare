from typing import List
from fastapi import HTTPException, status, APIRouter, Depends
from sqlalchemy.orm import Session

import src.repository.transform_posts as rep_transform
from src.database.connect import get_db
from src.database.models import User
from src.schemas_transform_posts import TransformImageModel, URLTransformImageResponse, SaveTransformImageModel, \
    TransformImageResponse
from src.services.auth import auth_service
from src.services.messages_templates import NOT_FOUND
from src.services.transform_posts import create_list_transformation
from src.services.cloudynary import get_transformed_url, get_qrcode

router = APIRouter(prefix='/image/transform', tags=['transform image'])


@router.get('/user', response_model=List[TransformImageResponse], status_code=status.HTTP_200_OK)
async def get_list_of_transformed_for_user(skip: int = 0, limit: int = 20,
                                           current_user: User = Depends(auth_service.get_current_user),
                                           db: Session = Depends(get_db)):
    """
    The get_list_of_transformed_for_user function returns a list of transformed images for the current user.
        The function takes in three parameters: skip, limit, and current_user.
        Skip is an integer that represents how many items to skip before returning results (defaults to 0).
        Limit is an integer that represents how many items to return after skipping (defaults to 20).
        Current_user is a User object representing the currently logged-in user.

    :param skip: int: Skip a number of items in the database
    :param limit: int: Limit the number of images returned
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass in the database session to the function
    :return: A list of all transformed images for the current user
    :doc-author: Trelent
    """
    return await rep_transform.get_all_transform_images_for_user(skip, limit, current_user, db)


@router.post('/{base_image_id}', response_model=URLTransformImageResponse, status_code=status.HTTP_200_OK)
async def transformation_for_image(base_image_id: int, body: TransformImageModel,
                                   current_user: User = Depends(
                                       auth_service.get_current_user),
                                   db: Session = Depends(get_db)):
    """
    The transformation_for_image function takes in a base_image_id, body, current_user and db. The function then
    calls the get_image_for transform method from the repos/transformations.py file to retrieve an image url for
    transformation. If no image is found with that id, it raises a 404 error message saying &quot;Image not
    found&quot;. Otherwise, it configures cloudinary using my api key and secret key (which I have hidden). It then
    creates a list of transformations based on what was passed into the body of this request (the user's desired
    transformations). Finally, it builds an url for that

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
    transform_list = create_list_transformation(body)
    url = get_transformed_url(image_url, transform_list)
    return {'url': url}


@router.post('/save/{base_image_id}', response_model=TransformImageResponse, status_code=status.HTTP_201_CREATED)
async def save_transform_image(base_image_id: int, body: SaveTransformImageModel,
                               current_user: User = Depends(auth_service.get_current_user),
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
async def get_qrcode_for_transform_image(transform_image_id: int,
                                         current_user: User = Depends(auth_service.get_current_user),
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
    qr_code = get_qrcode(image_url.photo_url)
    return qr_code


@router.get('/{transform_image_id}', response_model=TransformImageResponse, status_code=status.HTTP_200_OK)
async def get_transformed_image(transform_image_id: int, current_user: User = Depends(auth_service.get_current_user),
                                db: Session = Depends(get_db)):
    """
    The get_transformed_image function returns a transformed image by its id. The function takes in the
    transform_image_id as an integer and uses it to query the database for a transformed image. If no such image is
    found, then an HTTPException is raised with status code 404 and detail message NOT FOUND.

    :param transform_image_id: int: Get the image from the database
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the function
    :return: A transform image object
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
async def get_list_of_transformed_for_image(base_image_id: int, skip: int = 0, limit: int = 20,
                                            current_user: User = Depends(auth_service.get_current_user),
                                            db: Session = Depends(get_db)):
    """
    The get_list_of_transformed_for_image function returns a list of transformed images for the given base image. The
    function takes in an integer representing the id of the base image, and two optional parameters: skip and limit.
    Skip is used to specify how many results to skip before returning results, while limit specifies how many results
    should be returned at most.

    :param base_image_id: int: Get the base image id from the database
    :param skip: int: Skip the first n images in the list
    :param limit: int: Limit the number of results returned
    :param current_user: User: Get the current user from the database
    :param db: Session: Pass the database session to the function
    :return: A list of transformed images for a given base image
    """
    return await rep_transform.get_all_transform_images(base_image_id, skip, limit, current_user, db)
