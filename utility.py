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
