#!/usr/bin/env python
# coding=utf-8
#
# Copyright (C) [YEAR] [YOUR NAME], [YOUR EMAIL]
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
#
"""
Description of this extension
"""
import inkex
from inkex import Vector2d, DirectedLineSegment
import re
import bezier
import numpy as np

def produit_vectoriel(vecteur1, vecteur2):
    return vecteur1.x * vecteur2.y - vecteur1.y * vecteur2.x

class IntersectionLignes(inkex.EffectExtension):
    def effect(self):
        layer = self.svg.get_current_layer()
        segments = []

        for element in self.svg.xpath('//svg:path', namespaces=inkex.NSS):
            donnees = element.get('d')
            #self.msg(f"Données : {donnees}")

            points = self.extraire_points(donnees)
            #self.msg(f"Points : {points}")

            if len(points) < 2:
                continue

            for index in range(len(points) - 1):
                segment = DirectedLineSegment(points[index], points[index+1])
                segments.append(segment)

        for index1 in range(len(segments)):
            for index2 in range(index1+1, len(segments)):
                intersection = self.trouver_intersection(segments[index1], segments[index2])
                if intersection is not None:
                    #self.msg(f"Intersection entre {index1} et {index2} : {intersection}")
                    self.add_intersection_arrow(intersection, layer)

    def extraire_points(self, donnees):
        tokens = re.findall(r"[c]|[-+]?[0-9]*\.?[0-9]+(?:e[-+]?[0-9]+)?", donnees.replace(',', ' '))
        liste_points = []
        position = None
        commande = None
        i = 0
        while i < len(tokens):
            element = tokens[i]
            if element in "MmLlZz":
                commande = element
                i += 1
                if commande in "Zz":
                    if liste_points:
                        liste_points.append(liste_points[0])
                    continue
            else:
                try:
                    x = float(element)
                    y = float(tokens[i+1])
                except (IndexError, ValueError):
                    break
                i += 2
                if commande == 'm':
                    if position is None:
                        position = Vector2d(x, y)
                    else:
                        position = position + Vector2d(x, y)
                    liste_points.append(position)
                    commande = 'l'
                elif commande == 'M':
                    position = Vector2d(x, y)
                    liste_points.append(position)
                    commande = 'L'
                elif commande == 'l':
                    if position is None:
                        position = Vector2d(x, y)
                    else:
                        position = position + Vector2d(x, y)
                    liste_points.append(position)
                elif commande == 'L':
                    position = Vector2d(x, y)
                    liste_points.append(position)
        return liste_points

    def trouver_intersection(self, segment1, segment2):
        tolerance = 1e-9

        if ((abs(segment1.start.x - segment2.start.x) < tolerance and abs(segment1.start.y - segment2.start.y) < tolerance and
             abs(segment1.end.x - segment2.end.x) < tolerance and abs(segment1.end.y - segment2.end.y) < tolerance) or
            (abs(segment1.start.x - segment2.end.x) < tolerance and abs(segment1.start.y - segment2.end.y) < tolerance and
             abs(segment1.end.x - segment2.start.x) < tolerance and abs(segment1.end.y - segment2.start.y) < tolerance)):
            return (segment1.start, segment1.end)

        p = segment1.start
        r = segment1.end - segment1.start
        q = segment2.start
        s = segment2.end - segment2.start

        rxs = produit_vectoriel(r, s)

        if abs(rxs) < tolerance:
            if abs(produit_vectoriel(q - p, r)) < tolerance:
                r_dot_r = r.x * r.x + r.y * r.y
                if abs(r_dot_r) < tolerance:
                    if abs(segment2.start.x - p.x) < tolerance and abs(segment2.start.y - p.y) < tolerance:
                        return p
                    else:
                        return None
                t0 = ((q - p).x * r.x + (q - p).y * r.y) / r_dot_r
                t1 = (((segment2.end - p).x * r.x + (segment2.end - p).y * r.y)) / r_dot_r
                t_min = min(t0, t1)
                t_max = max(t0, t1)
                if t_max < 0 or t_min > 1:
                    return None
                else:
                    t_overlap_min = max(0, t_min)
                    t_overlap_max = min(1, t_max)
                    if abs(t_overlap_max - t_overlap_min) < tolerance:
                        return p + r * t_overlap_min
                    return (p + r * t_overlap_min, p + r * t_overlap_max)
            else:
                return None
        qmp = q - p
        t = produit_vectoriel(qmp, s) / rxs
        u = produit_vectoriel(qmp, r) / rxs

        if -tolerance <= t <= 1 + tolerance and -tolerance <= u <= 1 + tolerance:
            t = max(0, min(1, t))
            return p + r * t
        return None

    def add_intersection_arrow(self, point, parent):
        """
        Adds an arrow (a red triangle) at the given point.
        The arrow is defined with its tip at (0,0) so that after translation,
        the tip aligns with the intersection.
        """
        arrow = inkex.PathElement()
        arrow.set("d", "M0,0 L10,5 L10,-5 Z")
        arrow.style = {
            "stroke": "#ff0000",
            "stroke-width": "1",
            "fill": "#ff0000"
        }
        # Position the arrow so its tip is at the intersection point.
        arrow.transform = f"translate({point.x+6},{point.y})"
        parent.append(arrow)

if __name__ == '__main__':
    IntersectionLignes().run()
