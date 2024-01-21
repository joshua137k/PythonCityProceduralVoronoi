import numpy as np

def closest_point_on_line(point, line):
    x1, y1 = line[0]
    x2, y2 = line[1]
    x0, y0 = point

    A = x0 - x1
    B = y0 - y1
    C = x2 - x1
    D = y2 - y1

    dot = A * C + B * D
    len_sq = C * C + D * D

    if len_sq == 0:
        return x1, y1

    param = dot / len_sq

    if param < 0:
        return x1, y1
    elif param > 1:
        return x2, y2
    else:
        return x1 + param * C, y1 + param * D

def find_closest_line_to_point(point, polygon):
    min_distance = float('inf')
    closest_line = None

    for i in range(len(polygon)):
        line_start = polygon[i]
        line_end = polygon[(i + 1) % len(polygon)]
        closest_point = closest_point_on_line(point, [line_start, line_end])
        distance = np.linalg.norm(np.array(point) - np.array(closest_point))

        if distance < min_distance:
            min_distance = distance
            closest_line = [line_start, line_end]

    return closest_line

def find_polygon_center(polygon):
    """ Encontra o centro de um polígono. """
    if not polygon:
        return None
    polygon = np.array(polygon)
    centroid = np.mean(polygon, axis=0)
    return tuple(centroid)

def is_inside_polygon(x, y, vertices):
    """ Verifica se um ponto está dentro de um polígono. """
    n = len(vertices)
    inside = False
    if not vertices:
        return False

    p1x, p1y = vertices[0]
    for i in range(n + 1):
        p2x, p2y = vertices[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                        if p1x == p2x or x <= xinters:
                            inside = not inside
        p1x, p1y = p2x, p2y

    return inside

def grow_square_in_polygon(polygon):
    center = find_polygon_center(polygon)
    size = 1
    square = None

    while True:
        half_size = size / 4
        square = [(center[0] - half_size, center[1] - half_size),
                  (center[0] + half_size, center[1] - half_size),
                  (center[0] + half_size, center[1] + half_size),
                  (center[0] - half_size, center[1] + half_size)]

        if all(is_inside_polygon(x, y, polygon) for x, y in square):
            size += 0.5
        else:
            size -= 0.5
            half_size = size / 4
            square = [(center[0] - half_size, center[1] - half_size),
                    (center[0] + half_size, center[1] - half_size),
                    (center[0] + half_size, center[1] + half_size),
                    (center[0] - half_size, center[1] + half_size)]
            if not all(is_inside_polygon(x, y, polygon) for x, y in square):
                return None
            break

    return square
