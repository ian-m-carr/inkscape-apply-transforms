from inkex import Group, Transform, PathElement
from inkex.elements._polygons import EllipseBase, RectangleBase
from inkex.elements._groups import GroupBase

def bake_transforms_recursively(grp: Group, apply_to_paths=True, apply_to_shapes=True):
    """Bake transforms, i.e. each leaf node has the effective transform (starting
    from this group) set, and parent transforms are removed.

    .. versionadded:: 1.4

    Args:
        apply_to_paths (bool, optional): For path elements, the
            path data is transformed with its effective transform. Nodes and handles
            will have the same position as before, but visual appearance of the
            stroke may change (stroke-width is not touched). Defaults to True.
    """
    # pylint: disable=attribute-defined-outside-init
    transform: Transform
    replacements = dict()
    for element in grp:
        if isinstance(element, PathElement) and apply_to_paths:
            element.path = element.path.transform(grp.transform)
        elif isinstance(element, EllipseBase) or isinstance(element, RectangleBase) and apply_to_shapes:
            # generate a replacement path element and store it for mutation later
            new_element = element.to_path_element()
            new_element.path = new_element.path.transform(grp.transform @ element.transform)
            new_element.transform = None
            replacements[element] = new_element
        else:
            element.transform = grp.transform @ element.transform
            if isinstance(element, GroupBase):
                bake_transforms_recursively(element, apply_to_paths)
    grp.transform = None

    # now perform any replacements
    for key in replacements:
        rep = replacements[key]
        # add it to the parent
        key.getparent().add(rep)
        # and remove the old one
        key.delete()
