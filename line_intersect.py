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

def produit_vectoriel(vecteur1, vecteur2):
    return vecteur1.x * vecteur2.y - vecteur1.y * vecteur2.x

class IntersectionLignes(inkex.EffectExtension):
    def effect(self):
        layer = self.svg.get_current_layer()
        segments = []

        for element in self.svg.xpath('//svg:path', namespaces=inkex.NSS):
            donnees = element.get('d')

            # Vérifier si le chemin contient des courbes, et les ignorer
            if re.search(r"[CcQqSsTtAa]", donnees):
                continue

            points = self.extraire_points(donnees)

            # Ignorer les chemins avec moins de 2 points
            if len(points) < 2:
                continue

            for index in range(len(points) - 1):
                segment = DirectedLineSegment(points[index], points[index+1])
                segments.append(segment)

        # Vérification des intersections
        for index1 in range(len(segments)):
            for index2 in range(index1+1, len(segments)):
                intersection = self.trouver_intersection(segments[index1], segments[index2])
                if intersection is not None:
                    self.add_intersection_arrow(intersection, layer)

    def extraire_points(self, donnees):
        tokens = re.findall(r"[MmLlZz]|[-+]?[0-9]*\.?[0-9]+(?:e[-+]?[0-9]+)?", donnees.replace(',', ' '))
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
                        liste_points.append(liste_points[0])  # Fermer le tracé
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
                elif commande in ('l', 'L'):
                    if position is None:
                        position = Vector2d(x, y)
                    else:
                        position = position + Vector2d(x, y) if commande == 'l' else Vector2d(x, y)
                    liste_points.append(position)
        return liste_points

    def trouver_intersection(self, segment1, segment2):
        tolerance = 1e-9

        p, r = segment1.start, segment1.end - segment1.start
        q, s = segment2.start, segment2.end - segment2.start

        rxs = produit_vectoriel(r, s)
        qmp = q - p
        t = produit_vectoriel(qmp, s) / rxs if rxs else None
        u = produit_vectoriel(qmp, r) / rxs if rxs else None

        if rxs and -tolerance <= t <= 1 + tolerance and -tolerance <= u <= 1 + tolerance:
            t = max(0, min(1, t))
            return p + r * t
        return None

    def add_intersection_arrow(self, point, parent):
        """Ajoute un marqueur rouge aux intersections détectées."""
        arrow = inkex.PathElement()
        arrow.set("d", "M0,0 L10,5 L10,-5 Z")
        arrow.style = {
            "stroke": "#ff0000",
            "stroke-width": "1",
            "fill": "#ff0000"
        }
        arrow.transform = f"translate({point.x+6},{point.y})"
        parent.append(arrow)

if __name__ == '__main__':
    IntersectionLignes().run()
