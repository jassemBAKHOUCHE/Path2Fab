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
from shapely.geometry import Polygon
from svgpathtools import parse_path
from shapely.geometry import Polygon

class PolygonIntersect(inkex.EffectExtension):
    """An extension to set opacity of polygons to 0.20 when they intersect"""

    def effect(self):
        polygons = []
        for elem in self.document.getroot().iter():
            if isinstance(elem, inkex.PathElement):
                path = parse_path(elem.get('d'))
                if len(path) > 0:
                    coords = [(seg.start.real, seg.start.imag) for seg in path]
                    poly = Polygon(coords)
                    polygons.append((elem, poly))


        for i, (elem1, poly1) in enumerate(polygons):
            for j, (elem2, poly2) in enumerate(polygons):
                if i >= j:
                    continue
                if poly1.intersects(poly2):
                    self.set_opacity(elem1, 0.40)
                    self.set_opacity(elem2, 0.40)

    def set_opacity(self, element, opacity):
        if hasattr(element, 'style'):
            element.style['opacity'] = opacity

if __name__ == '__main__':
    PolygonIntersect().run()
