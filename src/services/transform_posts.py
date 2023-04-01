from typing import List
from src.schemas_transform_posts import TransformImageModel


def create_list_transformation(body: TransformImageModel) -> List[dict]:
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
            print('item', item)
            transform_list.append({'effect': f'{item.effect.name}:{item.strength}'})

    return transform_list