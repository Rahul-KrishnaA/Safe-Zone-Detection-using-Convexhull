from functools import cmp_to_key
import numpy as np

class Point:
    def __init__(self, x=None, y=None):
        self.x = x
        self.y = y

p0 = Point(0, 0)  # Global reference point for sorting

def nextToTop(S):
    return S[-2]

def distSq(p1, p2):
    return ((p1.x - p2.x) ** 2 + (p1.y - p2.y) ** 2)

def orientation(p, q, r):
    val = ((q.y - p.y) * (r.x - q.x) - (q.x - p.x) * (r.y - q.y))
    if val == 0:
        return 0  # Collinear
    elif val > 0:
        return 1  # Clockwise
    else:
        return 2  # Counterclockwise

def compare(p1, p2):
    o = orientation(p0, p1, p2)
    if o == 0:
        return -1 if distSq(p0, p2) >= distSq(p0, p1) else 1
    return -1 if o == 2 else 1

def compute_convex_hull(points):
    global p0
    point_objects = [Point(lat, lon) for lat, lon in points]

    ymin = point_objects[0].y
    min_index = 0
    for i in range(1, len(point_objects)):
        if (point_objects[i].y < ymin or
            (ymin == point_objects[i].y and point_objects[i].x < point_objects[min_index].x)):
            ymin = point_objects[i].y
            min_index = i

    point_objects[0], point_objects[min_index] = point_objects[min_index], point_objects[0]
    p0 = point_objects[0]
    point_objects = sorted(point_objects, key=cmp_to_key(compare))

    m = 1
    for i in range(1, len(point_objects)):
        while (i < len(point_objects) - 1 and 
               orientation(p0, point_objects[i], point_objects[i + 1]) == 0):
            i += 1
        point_objects[m] = point_objects[i]
        m += 1

    if m < 3:
        raise ValueError("Convex hull is not possible with less than 3 unique points.")

    S = [point_objects[0], point_objects[1], point_objects[2]]
    for i in range(3, m):
        while len(S) > 1 and orientation(nextToTop(S), S[-1], point_objects[i]) != 2:
            S.pop()
        S.append(point_objects[i])

    return np.array([(p.x, p.y) for p in S])
    