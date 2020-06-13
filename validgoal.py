# -------------------------------------------------------
# Assignment (1)
# Written by (Mohamed Hefny, 40033382)
# For COMP 472 Section (ABIX) – Summer 2020
# --------------------------------------------------------
def valid_goal(map, goal):
    """
    Checks if the goal is a valid point, it makes the algorithm faster
    parameter map: 2d array of the graph
    parameter goal: the goal of the graph
    """
    row, col = goal
    height_, width_ = map.shape

    # if the end point is out of the map, return infinity
    if col < 0 or row < 0 or col > width_ or row > height_:
        return False

    # bottom edge
    if row == 0:
        if col == 0:
            return map[0, 0] == 0
        if col == width_:
            return map[0, width_ - 1] == 0
        return map[0, col - 1] == 0 or map[0, col] == 0

    # top edge
    if row == height_:
        if col == 0:
            return map[height_ - 1, 0] == 0
        if col == width_:
            return map[height_ - 1, width_ - 1] == 0
        return map[height_ - 1, col - 1] == 0 or map[height_ - 1, col] == 0

    # left edge
    if col == 0:
        return map[row - 1, 0] == 0 or map[row, 0] == 0

    # right edge
    if col == width_:
        return map[row - 1, width_ - 1] == 0 or map[row, width_ - 1] == 0

    # internal
    return map[row - 1, col - 1] == 0 or map[row, col - 1] == 0 \
           or map[row - 1, col] == 0 or map[row, col] == 0

#credits for helping: from dung hoang

