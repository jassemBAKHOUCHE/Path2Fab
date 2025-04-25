import inkex
import sys
sys.path.append('libs')
import numpy as np
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


class BezierIntersection(inkex.EffectExtension):
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
                    self.draw_cross(pt, layer)

    def draw_cross(self, pt, parent):
        group = etree.SubElement(parent, inkex.addNS('g', 'svg'))
        line1 = etree.SubElement(group, inkex.addNS('path', 'svg'))
        line2 = etree.SubElement(group, inkex.addNS('path', 'svg'))
        d1 = f"M {pt[0]-2},{pt[1]-2} L {pt[0]+2},{pt[1]+2}"
        d2 = f"M {pt[0]+2},{pt[1]-2} L {pt[0]-2},{pt[1]+2}"
        for line, d in [(line1, d1), (line2, d2)]:
            line.set('d', d)
            line.set('style', 'stroke:#f00;stroke-width:1')


if __name__ == '__main__':
    BezierIntersection().run()
