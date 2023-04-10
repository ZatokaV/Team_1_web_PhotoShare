from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field


class TransformImageResponse(BaseModel):
    id: int
    photo_url: str
    photo_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class TypeResizeImage(str, Enum):
    crop = 'crop'
    scale = 'scale'
    fill = 'fill'
    pad = 'pad'
    thumb = 'thumb'
    fit = 'fit'
    fill_pad = 'fill_pad'


class GravityImage(str, Enum):
    auto = 'auto'
    face = 'face'
    center = 'center'
    north = 'north'
    west = 'west'
    east = 'east'
    south = 'south'
    north_west = 'north_west'
    north_east = 'north_east'
    south_west = 'south_west'
    south_east = 'south_east'


class PercentImage(float):
    percent: float = Field(ge=0, le=1)


class TransformCropModel(BaseModel):
    width: int | PercentImage
    height: int | PercentImage
    crop: Optional[TypeResizeImage]
    gravity: Optional[GravityImage]
    background: Optional[str]


class RadiusImageModel(BaseModel):
    all: int = Field(ge=0, default=0)
    left_top: int = Field(ge=0, default=0)
    right_top: int = Field(ge=0, default=0)
    right_bottom: int = Field(ge=0, default=0)
    left_bottom: int = Field(ge=0, default=0)
    max: bool = Field(default=False)


class RotateImageModel(BaseModel):
    degree: int = Field(ge=-360, le=360, default=0)


class TypeArtEffect(str, Enum):
    al_dente = 'al_dente'
    athena = 'athena'
    audrey = 'audrey'
    aurora = 'aurora'
    daguerre = 'daguerre'
    eucalyptus = 'eucalyptus'
    fes = 'fes'
    frost = 'frost'
    hairspray = 'hairspray'
    hokusai = 'hokusai'
    incognito = 'incognito'
    linen = 'linen'
    peacock = 'peacock'
    primavera = 'primavera'
    quartz = 'quartz'
    red_rock = 'red_rock'
    refresh = 'refresh'
    sizzle = 'sizzle'
    sonnet = 'sonnet'
    ukulele = 'ukulele'
    zorro = 'zorro'


class ArtEffectTransformModel(BaseModel):
    effect: TypeArtEffect


class SimpleEffectType(str, Enum):
    grayscale = 'grayscale'
    negate = 'negative'
    cartoonify = 'cartoonify'
    oil_paint = 'oil_paint'
    blackwhite = 'black_white'


class SimpleEffectTransformModel(BaseModel):
    effect: SimpleEffectType
    strength: int = Field(ge=0, le=100)


class TypeContrast(str, Enum):
    contrast = 'contrast'
    brightness = 'brightness'


class ContrastEffectTransformModel(BaseModel):
    effect: TypeContrast
    level: int = Field(ge=-100, le=100)


class TypeBlurEffect(str, Enum):
    blur: 'blur'
    blur_faces = 'blur_faces'
    blur_region = 'blur_region'


class BlurEffectTransformModel(BaseModel):
    effect: TypeBlurEffect
    strength: int = Field(ge=0, le=2000)
    x: Optional[int] = Field(ge=0)
    y: Optional[int] = Field(ge=0)
    width: Optional[int] = Field(ge=0)
    height: Optional[int] = Field(ge=0)


class TransformImageModel(BaseModel):
    resize: Optional[TransformCropModel]
    rotate: Optional[RotateImageModel]
    radius: Optional[RadiusImageModel]
    art_effect: Optional[ArtEffectTransformModel]
    simple_effect: Optional[List[SimpleEffectTransformModel]]
    contrast_effect: Optional[List[ContrastEffectTransformModel]]
    blur_effect: Optional[List[BlurEffectTransformModel]]


class URLTransformImageResponse(BaseModel):
    url: str = ''


class SaveTransformImageModel(BaseModel):
    url: str
