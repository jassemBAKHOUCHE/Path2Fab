"""
Check if an object is isolated 
"""

import inkex
import sys
import math 

"""
Calcul the distance between two points in a Euclidian plan (jsp comment ont dit quand on a le graph euclidien... a voir)
Parameters : 
    a : start point, a tuple (x, y)
    b : end point, a tuple (x, y)
Return : 
    The distance in the same unit as the coordinates of points a and b 
"""
def distance(a, b):
    pass
    xa = a[0]
    ya = a[1]
    xb = b[0]
    yb = b[1]
    distance = math.sqrt(((xb-xa)**2) + ((yb-ya)**2))
    return distance

class IsolatedElement(inkex.EffectExtension):
    def add_arguments(self, pars):
        # Ajouter un argument pour exclure certains calques/objets
        pars.add_argument('--exclude_layers', type=str, default="layer1,svg1,namedview1,defs1", help="Liste des objets à exclure séparés par des virgules")

    def effect(self):
        tab_ids = []
        tab_minimum = []
        tab_paths = []

        # retrieve layers/objects to exclude
        exclude_layers = set(self.options.exclude_layers.split(','))
        # for each element in the project
        for elem in self.document.getroot().iter():
            # ignore elements without ID or excluded layers/objects
            if not elem.get_id() or elem.get_id() in exclude_layers:
                continue
            # check if the element if a graphic form
            if isinstance(elem, inkex.ShapeElement):
                # the bounding box 
                bbox = elem.bounding_box()
                center_x = bbox.center_x
                center_y = bbox.center_y
                # to find the smallest distance between all of them 
                smallest = math.inf

                # for each other element in the project
                for elem_other in self.document.getroot().iter():
                    # ignore elements without ID or excluded layers/objects
                    if not elem.get_id() or elem.get_id() in exclude_layers:
                        continue
                    # check if the element if a graphic form and the other element we are looking at is not the same element as the previous one
                    if isinstance(elem_other, inkex.ShapeElement) and (elem.get_id() != elem_other.get_id()):
                        # the bounding box 
                        bbox_other = elem_other.bounding_box()
                        center_x_other = bbox_other.center_x
                        center_y_other = bbox_other.center_y
                        # we calcul the distance between these two elements 
                        distance_point = distance((center_x, center_y), (center_x_other, center_y_other))
                        # smallest 
                        if(distance_point < smallest):
                            smallest = distance_point
                
                # stock in tabs 
                tab_minimum.append(smallest)
                tab_ids.append(elem.get_id())

        nb_element = len(tab_ids) 
        # we calculate the average minimum
        ave = 0
        for k in range(0, nb_element):
            ave += tab_minimum[k]
        average = ave / nb_element

        # check for each element if the smallest distance between it and the others is smaller than 2 times the average minimum
        for i in range(0, nb_element):
            if tab_minimum[i] > average*2:
                tab_paths.append(tab_ids[i])

        # create a good print 
        if len(tab_paths) == 0:
            sys.stderr.write('No element is isolated.\n')
        else :
            if tab_paths[0]:
                paths = tab_paths[0]
            for i in range(1, len(tab_paths)) :
                paths += ", " + tab_paths[i]
            sys.stderr.write(f'Warning : the next elements are isolated.\nElements involved : {paths}\nYou can find these elements in your project\'s layers.')


if __name__ == '__main__':
    IsolatedElement().run()
