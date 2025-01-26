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
                    """
                    sys.stderr.write(f'width : {width}\n')
                    sys.stderr.write(f'height : {height}\n')
                    sys.stderr.write(f'id : {elem.get_id()}\n')
                    sys.stderr.write(f'The selected elements are too small for the laser cuter.\n')
                    """
                    #self.svg.selection.add(elem.get_id())

        # create a good print 
        if len(tab_paths) == 0:
            sys.stderr.write('No element is too small for the laser cuter.')
        else :
            if tab_paths[0]:
                paths = tab_paths[0]
            for i in range(1, len(tab_paths)) :
                paths += ", " + tab_paths[i]
            sys.stderr.write(f'The next elements are too small for the laser cuter.\nTheir width and heigth have to be greater than {limit_size} mm to be accepted.\nElements involved : {paths}\nYou can find these elements in your project\'s layers.')

if __name__ == '__main__':
    TooSmallObject().run()
