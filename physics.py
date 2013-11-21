"""
author: Mike McMahon

created: 11/13/13

"""


def collision_detection(rect, point):
    """
        Does a single point lay within the given rectangle
    """
    x, y, w, h = rect
    x2, y2 = point

    if x <= x2 <= x + w:
        if y <= y2 <= y + h:
            return True

    return False