from scipy import spatial
import math
import numpy as np


def calculate_distance_without_sqrt(point1, point2):
    return (point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2  # for speed


def euclidian_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0]) ** 2 + (point1[1] - point2[1]) ** 2)


def find_closest_point(middle_pixel_path, point):
    path_pixels = np.asarray(middle_pixel_path)
    x = path_pixels[spatial.KDTree(path_pixels).query(point)[1]]
    return tuple(x)
# Copied from the ptext library
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points