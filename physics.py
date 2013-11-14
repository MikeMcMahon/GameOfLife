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


def collision_detection_rect(rect1, rect2):
    """
    If the second rectangle lands anywhere on top of the first rectangle
    """
    x, y, w, h = rect2
    ul = x, y
    ur = x+w, y
    bl = x, y+h
    br = x+w, y+h

    if collision_detection(rect1, ul):
        return True
    if collision_detection(rect1, ur):
        return True
    if collision_detection(rect1, bl):
        return True
    if collision_detection(rect1, br):
        return True

    return False