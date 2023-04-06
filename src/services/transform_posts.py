from typing import List

from src.schemas_transform_posts import TransformImageModel


def create_list_transformation(body: TransformImageModel) -> List[dict]:
    """
    The create_list_transformation function takes in a TransformImageModel object and returns a list of dictionaries.
    Each dictionary represents an image transformation that will be applied to the original image. The function iterates
    through each attribute of the TransformImageModel object, checking if it is not None (i.e., has been set by the user).
    If so, it creates a dictionary with key-value pairs representing parameters for that particular transformation.

    :param body: TransformImageModel: Create a list of dictionaries that are used to transform the image
    :return: A list of dictionaries that can be used to create a transformation
    """
    transform_list = []

    if body.resize:
        transform_item = {}
        t_dict = body.resize.dict()
        for key in t_dict:
            if t_dict[key]:
                if type(t_dict[key]) not in (int, str):
                    transform_item[key] = t_dict[key].name
                else:
                    transform_item[key] = t_dict[key]
        transform_list.append(transform_item)

    if body.rotate:
        transform_list.append({'angle': body.rotate.degree})

    if body.radius:
        if body.radius.max:
            transform_list.append({'radius': 'max'})
        elif body.radius.all > 0:
            transform_list.append({'radius': body.radius.all})
        else:
            transform_list.append({'radius': f'{body.radius.left_top}:{body.radius.right_top}:'
                                             f'{body.radius.right_bottom}:{body.radius.left_bottom}'})

    if body.art_effect:
        transform_list.append({'effect': f'art:{body.art_effect.effect.name}'})

    if body.simple_effect:
        for item in body.simple_effect:
            transform_list.append({'effect': f'{item.effect.name}:{item.strength}'})

    if body.contrast_effect:
        for item in body.contrast_effect:
            transform_list.append({'effect': f'{item.effect.name}:{item.level}'})

    if body.blur_effect:
        for item in body.blur_effect:
            transform_item = {}
            t_dict = item.dict()
            transform_item['effect'] = f'{item.effect.name}:{item.strength}'
            for key in t_dict:
                if t_dict[key] and key != 'strength' and key != 'effect':

                    if type(t_dict[key]) not in (int, str):
                        transform_item[key] = t_dict[key].name
                    else:
                        transform_item[key] = t_dict[key]
            transform_list.append(transform_item)
    return transform_list
