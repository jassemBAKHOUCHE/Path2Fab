"""
Check if an object is too small for a laser cutter 
"""

import inkex
import sys

class TooSmallObject(inkex.EffectExtension):
    def effect(self):
        limit_size = 1.0
        tab_paths = []
        for elem in self.document.getroot().iter():
            # check if the element if a graphic form
            if isinstance(elem, inkex.ShapeElement):
                # the bounding box 
                bbox = elem.bounding_box()
                # dimensions
                width, height = bbox.width, bbox.height
                if width < limit_size or height < limit_size :
                    tab_paths.append(elem.get_id())
                    self.svg.selection.add(elem.get_id())

        # create a good print 
        if len(tab_paths) == 0:
            sys.stderr.write('No element is too small for the laser cuter.')
        else :
            if tab_paths[0]:
                paths = tab_paths[0]
            for i in range(1, len(tab_paths)) :
                paths += ", " + tab_paths[i]
            sys.stderr.write(f'Les éléments suivants sont trop petits pour la découpeuse laser.\nLeurs longeur et largeur doivent être inférieur à {limit_size} mm pour être acceptés.\nEléments impliqués : {paths}\nVous pouvez trouver ces éléments dans les calques de votre projet.')

if __name__ == '__main__':
    TooSmallObject().run()

