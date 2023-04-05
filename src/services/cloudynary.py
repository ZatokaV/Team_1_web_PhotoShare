import cloudinary
import base64
import io
import qrcode
import qrcode.image.base
import qrcode.image.svg

from src.conf.config import settings

cloudinary.config(
        cloud_name=settings.cloudinary_name,
        api_key=settings.cloudinary_api_key,
        api_secret=settings.cloudinary_api_secret,
        secure=True
    )


def get_url(image_url: str):
    return cloudinary.CloudinaryImage(image_url).build_url()

def get_transformed_url(image_url: str, transform_list: list[dict]):
    """
    The get_transformed_url function takes in an image_url and a list of transformations,
    and returns the url for the transformed image.


    :param image_url: str: Specify the image to be transformed
    :param transform_list: list[dict]: Specify the transformations that will be applied to the image
    :return: A url string with the transformations applied
    """
    return cloudinary.CloudinaryImage(image_url).build_url(transformation=transform_list)


def get_qrcode(photo_url: str):
    """
    The get_qrcode function takes a photo_url as an argument and returns the QR code for that URL.
    The function uses the qrcode library to create a QR code object from the photo_url, then saves it to a buffer.
    The buffer is encoded in base64 and returned as a string.

    :param photo_url: str: Tell the function what type of data to expect
    :return: A base64 encoded string of a qr code image
    """
    qr = qrcode.make(photo_url)
    buf = io.BytesIO()
    qr.save(buf)
    qr_code = base64.b64encode(buf.getvalue()).decode('ascii')
    return qr_code
