import math
import inkex
import numpy as np
from drawArrow import ImageWithLineWindow
from inkex.paths import CubicSuperPath
from lxml import etree
from svgpathtools import parse_path

def bezier_bbox(curve):
    points = np.array(curve)
    min_pt = np.min(points, axis=0)
    max_pt = np.max(points, axis=0)
    return min_pt, max_pt


def bboxes_intersect(b1, b2):
    (min1, max1), (min2, max2) = b1, b2
    return not (
        max1[0] < min2[0] or max2[0] < min1[0] or
        max1[1] < min2[1] or max2[1] < min1[1]
    )


def subdivide_bezier(P, t):
    P01 = (1 - t) * P[0] + t * P[1]
    P12 = (1 - t) * P[1] + t * P[2]
    P23 = (1 - t) * P[2] + t * P[3]
    P012 = (1 - t) * P01 + t * P12
    P123 = (1 - t) * P12 + t * P23
    P0123 = (1 - t) * P012 + t * P123
    return [P[0], P01, P012, P0123], [P0123, P123, P23, P[3]]


def recursive_intersection(c1, c2, depth=10, tol=1.0):
    if depth == 0:
        mid = (c1[0] + c1[3] + c2[0] + c2[3]) / 4
        return [mid]

    if not bboxes_intersect(bezier_bbox(c1), bezier_bbox(c2)):
        return []

    c1a, c1b = subdivide_bezier(c1, 0.5)
    c2a, c2b = subdivide_bezier(c2, 0.5)

    return (
        recursive_intersection(c1a, c2a, depth-1, tol) +
        recursive_intersection(c1a, c2b, depth-1, tol) +
        recursive_intersection(c1b, c2a, depth-1, tol) +
        recursive_intersection(c1b, c2b, depth-1, tol)
    )


class BezierIntersect(inkex.EffectExtension):
    def __init__(self):
        super().__init__()
        self.fileName = self.document_path()
        self.arrows = []

    def effect(self):
        layer = self.svg.get_current_layer()
        paths = self.svg.xpath('//svg:path', namespaces=inkex.NSS)
        curves = []

        for path_idx, path in enumerate(paths):
            d = path.get('d')
            p = parse_path(path.get('d'))
            if not d or (len(p) > 2 and p[0].start == p[-1].end):  # not d -> pas de donnée dans le path
                continue
            csp = CubicSuperPath(d)
            for subpath_idx, subpath in enumerate(csp):
                prev_point = np.array(subpath[0][1])
                for seg_idx, ctl in enumerate(subpath):
                    P0 = prev_point
                    P1 = np.array(ctl[0])
                    P2 = np.array(ctl[1])
                    P3 = np.array(ctl[2])
                    curves.append([P0, P1, P2, P3])
                    prev_point = P3

        seen_points = []
        epsilon = 0.8   # deux intersection inferieure -> la meme intersection

        def is_close(pt1, pt2):
            return np.linalg.norm(np.array(pt1) - np.array(pt2)) < epsilon

        for i in range(len(curves)):
            for j in range(i + 2, len(curves)):
                intersections = recursive_intersection(curves[i], curves[j])
                unique_pts = []
                for pt in intersections:
                    if not any(is_close(pt, seen) for seen in seen_points):
                        seen_points.append(pt)
                        unique_pts.append(pt)
                for pt in unique_pts:
                    arrow_size = 5
                    center_x, center_y = pt[0], pt[1]
                    start_x = center_x + 5
                    start_y =  center_y + 5
                    
                    angle = math.atan2(center_y - start_y, center_x - start_x)
                    left_x = center_x - arrow_size * math.cos(angle - math.pi / 6)
                    left_y = center_y - arrow_size * math.sin(angle - math.pi / 6)
                    right_x = center_x - arrow_size * math.cos(angle + math.pi / 6)
                    right_y = center_y - arrow_size * math.sin(angle + math.pi / 6)
                    self.arrows.append([start_x, start_y, center_x, center_y, left_x, left_y, right_x, right_y])

        self.msg(f"INTERSECTIONS DE COURBES DE BEZIER : Nombre d'erreur(s) trouvée(s) : {len(self.arrows)}\n\n")
                    


if __name__ == '__main__':
    BezierIntersect().run()
    ink = BezierIntersect()
    ink.run()
    win = ImageWithLineWindow(ink.fileName, ink.arrows, "bezier_intersections.jpg") 

