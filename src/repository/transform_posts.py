from sqlalchemy.orm import Session

# from src.database.models import Post


async def get_image_for_transform(image_id: int, db: Session) -> str | None:
    # image = db.query(Post).filter(Post.id == image_id).first() error in models
    image = None
    image_path = None
    if image:
        image_path = image.photo_url
    return image_path


async def set_transform_image(image_id: int, modify_url: str, db: Session) : #-> Post | None:
    #image = db.query(Post).filter(Post.id == image_id).first()
    image = None
    if image:
        image.photo_url = modify_url
        db.commit()
    return image



