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


def get_transformed_url(image_url: str, transform_list: list[dict]):
    return cloudinary.CloudinaryImage(image_url).build_url(transformation=transform_list)


def get_qrcode(photo_url: str):
    qr = qrcode.make(photo_url)
    buf = io.BytesIO()
    qr.save(buf)
    qr_code = base64.b64encode(buf.getvalue()).decode('ascii')
    return qr_code
