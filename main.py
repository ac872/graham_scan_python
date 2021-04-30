from math import atan2
import numpy as np
import matplotlib.pyplot as plt


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


def graham_scan(coords):
    """Sort list so that first point is the lowest point in the numpy array"""
    coords = coords[np.argsort(coords[:, -1])]
    if len(coords) <= 4:
        raise RuntimeError("Convex hull not possible with less than three points")
    try:
        if coords[0][1] == coords[1][1]:
            """Sort by the y value then the x value if two y values are the same to find leftmost point"""
            coords = coords[np.lexsort((coords[:, 0], coords[:, 1]))]
    except IndexError:
        raise RuntimeError("Convex Hull not possible with less than three points")
    """Get Lowest Point then remove from the numpy array"""
    lowest_point = coords[0]
    p0 = Point(lowest_point[0], lowest_point[1])
    coords = coords[1:]     # Remove first value which is lowest point
    coords = np.array([[x, y, polar_angle(p0, Point(x, y))] for (x, y) in zip(coords.flat[0::2], coords.flat[1::2])])
    """Sort By Polar Angle W.R.T lowest point p0"""
    coords = coords[np.argsort(coords[:, -1])]
    coords = coords[:, [0, 1]]  # Remove polar angle once sorted
    coords = [Point(x, y) for (x, y) in zip(coords.flat[0::2], coords.flat[1::2])]
    sorted_points = coords
    hull = [p0, sorted_points[0]]
    del sorted_points[0]
    for point in sorted_points:
        while orientation(point, hull[-1], hull[-2]) <= 0:
            hull.pop()
        hull.append(point)

    return hull


def orientation(a, b, c):
    return (b.y - a.y) * (c.x - b.x) - (b.x - a.x) * (c.y - b.y)


def polar_angle(p0, p1):
    return atan2(p1.y - p0.y, p1.x - p0.x)


def benchmark(test_sizes):
    for size in test_sizes:
        coordinates = np.random.rand(size, 2)
        coords = [Point(x, y) for (x, y) in zip(coordinates.flat[0::2], coordinates.flat[1::2])]
        x_vals = [i.x for i in coords]
        y_vals = [i.y for i in coords]
        hull = graham_scan(coordinates)
        hull_x_vals = [i.x for i in hull]
        hull_y_vals = [i.y for i in hull]
        plt.scatter(x_vals, y_vals, color='green')
        plt.scatter(hull_x_vals, hull_y_vals, color='red')
        plt.show()


if __name__ == "__main__":
    sizes = [10, 50, 75, 100, 1000]
    benchmark(sizes)
