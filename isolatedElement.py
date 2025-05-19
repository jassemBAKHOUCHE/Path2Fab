"""
Check if an object is isolated 
"""

import inkex
import sys
import math 
from drawArrow import ImageWithLineWindow
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

"""
Calcul the distance between two points in a Euclidian plan
Parameters : 
    a : start point, a tuple (x, y)
    b : end point, a tuple (x, y)
Return : 
    The distance in the same unit as the coordinates of points a and b 
"""
def distance(a, b):
    return math.sqrt(((b[0]-a[0])**2) + ((b[1]-a[1])**2))

"""
Find the good distance between two objects, takes account of the size of objects 
Parameters : 
    bboxObj1 : the bounding box of the first object 
    bboxObj2 : the bounding box of the second object 
Return : 
    The distance in the same unit as the coordinates in the bounding box
"""
def findGoodDistance(bboxObj1, bboxObj2):
    # we find the area where Obj2 is in relation to Obj1
    area = findArea(bboxObj1, bboxObj2)

    # we find the good vector depending of the area 
    match area : 
        # comparing the smallest distance between 3 possibilities in the area : the corner, the center on Y axis, the center on X axis 
        case "TR" : return min([distance((bboxObj1.right, bboxObj1.top), (bboxObj2.left, bboxObj2.bottom)),          # corner top right - corner left bottom
                                distance((bboxObj1.center_x, bboxObj1.top), (bboxObj2.center_x, bboxObj2.bottom)),   # center top - center bottom
                                distance((bboxObj1.right, bboxObj1.center_y), (bboxObj2.left, bboxObj2.center_y))])  # center right - center left
        
        case "TL" : return min([distance((bboxObj1.right, bboxObj1.top), (bboxObj2.right, bboxObj2.bottom)),         # corner top left - corner bottom right
                                distance((bboxObj1.center_x, bboxObj1.top), (bboxObj2.center_x, bboxObj2.bottom)),   # center top - center bottom
                                distance((bboxObj1.left, bboxObj1.center_y), (bboxObj2.right, bboxObj2.center_y))])  # center left - center right
        
        case "BR" : return min([distance((bboxObj1.right, bboxObj1.bottom), (bboxObj2.left, bboxObj2.top)),          # corner bottom right - corner top left
                                distance((bboxObj1.center_x, bboxObj1.bottom), (bboxObj2.center_x, bboxObj2.top)),   # center bottom - center top
                                distance((bboxObj1.right, bboxObj1.center_y), (bboxObj2.left, bboxObj2.center_y))])  # center right - center left
        
        case "BL" : return min([distance((bboxObj1.left, bboxObj1.bottom), (bboxObj2.right, bboxObj2.top)),          # corner bottom left - corner top right
                                distance((bboxObj1.center_x, bboxObj1.bottom), (bboxObj2.center_x, bboxObj2.top)),   # center bottom - center top 
                                distance((bboxObj1.left, bboxObj1.center_y), (bboxObj2.right, bboxObj2.center_y))])  # center left - center right 
        case default : return 0

"""
Find the area where Obj2 is in relation to Obj1 
Parameters : 
    bboxObj1 : the bounding box of the first object 
    bboxObj2 : the bounding box of the second object 
Return : 
    two letters which represent the area (comparaison based on the center of the first object) -> TR (top right), TL (top left), BR (bottom right), BL (bottom left)
"""
def findArea(bboxObj1, bboxObj2):
    center1X = bboxObj1.center_x
    center1Y = bboxObj1.center_y
    center2X = bboxObj2.center_x
    center2Y = bboxObj2.center_y
    if center2X >= center1X and center2Y <= center1Y : 
        return "TR"
    elif center2X <= center1X and center2Y <= center1Y  : 
        return "TL"
    elif center2X >= center1X and center2Y >= center1Y  : 
        return "BR"
    elif center2X <= center1X and center2Y >= center1Y  :  
        return "BL"
    else : 
        return "None"

"""
Find if two object have an intersection or not 
"""
def intersection(Axtl, Aytl, Awidth, Aheight, Bxtl, Bytl, Bwidth, Bheight):
    return  (Axtl+Awidth) >= Bxtl and (Bxtl+Bwidth) >= Axtl and (Aytl+Aheight) >= Bytl and (Bytl+Bheight) >= Aytl

class IsolatedElement(inkex.EffectExtension):
    def __init__(self):
            super().__init__()
            self.fileName = self.document_path()
            self.arrows = []

    def add_arguments(self, pars):
        # add argument to exclude layers
        pars.add_argument('--exclude_layers', type=str, default="layer1,svg1,namedview1,defs1", help="Comma-separated list of objects to exclude")

    def effect(self):
        tab_ids = [] # ids of elements suspected of being too far 
        tab_minimum = [] # minimum distance from another element for each element in order 
        tab_paths = [] # ids of those which are realy too far 
        tab_noInPage = [] # ids of those which are not in the page 
        page_width = self.svg.unittouu(self.svg.attrib.get('width')) # page width 
        page_height = self.svg.unittouu(self.svg.attrib.get('height')) # page height

        # retrieve layers/objects to exclude
        exclude_layers = set(self.options.exclude_layers.split(','))
        # for each element in the project
        for elem in self.document.getroot().iter():
            # ignore elements without ID or excluded layers/objects
            if not elem.get_id() or elem.get_id() in exclude_layers:
                continue

            # check if the element if a graphic form
            if isinstance(elem, inkex.ShapeElement) and not (isinstance(elem, inkex.elements._groups.Layer)):

                try : 
                    # the bounding box 
                    bbox = elem.bounding_box()

                    # case the object is not in the page 
                    if not intersection(bbox.left, bbox.top, bbox.width, bbox.height, 0, 0, page_width, page_height):
                        tab_noInPage.append(elem.get_id())
                        continue

                    # to find the smallest distance between all of them 
                    smallest = math.inf

                    # for each other element in the project, we are looking for the smallest distance it have with another element 
                    for elem_other in self.document.getroot().iter():
                        # ignore elements without ID or excluded layers/objects
                        if not elem.get_id() or elem.get_id() in exclude_layers:
                            continue

                        # check if the element if a graphic form and the other element we are looking at is not the same element as the previous one
                        if isinstance(elem_other, inkex.ShapeElement) and (elem.get_id() != elem_other.get_id()) and not (isinstance(elem_other, inkex.elements._groups.Layer)):
                            # the bounding box 
                            bbox_other = elem_other.bounding_box()
                            
                            # if the object have an intersection with an other object -> not isolated 
                            if intersection(bbox.left, bbox.top, bbox.width, bbox.height, bbox_other.left, bbox_other.top, bbox_other.width, bbox_other.height):
                                smallest = 0
                                break

                            # calcul the distance between these two elements (the closed one to the real one)
                            distance_point = findGoodDistance(bbox, bbox_other)
                            # smallest 
                            if(distance_point < smallest):
                                smallest = distance_point 


                        arrow_size = 5
                        arr_pos = []
                        if bbox:
                            
                            center_x, center_y = bbox.left, bbox.top 
                            start_x = center_x + 5
                            start_y =  center_y + 5
                            
                            angle = math.atan2(center_y - start_y, center_x - start_x)
                            left_x = center_x - arrow_size * math.cos(angle - math.pi / 6)
                            left_y = center_y - arrow_size * math.sin(angle - math.pi / 6)
                            right_x = center_x - arrow_size * math.cos(angle + math.pi / 6)
                            right_y = center_y - arrow_size * math.sin(angle + math.pi / 6)
                            arr_pos =  [start_x, start_y, center_x, center_y, left_x, left_y, right_x, right_y]
                    
                    # stock in tabs  
                    tab_minimum.append(smallest)
                    tab_ids.append((elem.get_id(), arr_pos))

                except Exception:
                    continue

        nb_element = len(tab_ids) 
        # calcul the average minimum
        ave = 0
        if nb_element != 0:
            cptZero = 0
            for k in range(0, nb_element):
                ave += tab_minimum[k]
                if tab_minimum[k] == 0 : # we don't count those who are intersected
                    cptZero += 1
            if nb_element - cptZero > 0 :
                average = ave / (nb_element - cptZero)
                
                # check for each element if the smallest distance between itself and the others is smaller than 2 times the average minimum
                for i in range(0, nb_element):
                    if tab_minimum[i] > average*2:
                        tab_paths.append(tab_ids[i])
        # create a good print :
        # isolated object 
        if len(tab_paths) == 0:
            sys.stderr.write('Aucun élément est isolé.\n')
        else :
            if tab_paths[0]:
                paths = tab_paths[0][0]
                self.arrows.append(tab_paths[0][1])
            for i in range(1, len(tab_paths)) :
                paths += ", " + tab_paths[i][0]
                self.arrows.append(tab_paths[i][1])
            sys.stderr.write(f'Attention : les éléments suivants sont isolés.\nEléments impliqués : {paths}\nVous pouvez trouver ces éléments dans les calques de votre projet.\n')
            self.msg(f"OBJETS ISOLES : Nombre d'erreur(s) trouvée(s) : {len(self.arrows)}\n\n")
        # object out of the page 
        if len(tab_noInPage) == 0:
            sys.stderr.write('Aucun élément est en dehors de la page.\n')
        else :
            if tab_noInPage[0]:
                paths = tab_noInPage[0]
            for i in range(1, len(tab_noInPage)) :
                paths += ", " + tab_noInPage[i]
            sys.stderr.write(f'Attention : les éléments suivants sont en dehors de la page.\nEléments impliqués : {paths}\nVous pouvez trouver ces éléments dans les calques de votre projet.')


if __name__ == '__main__':
    ink =  IsolatedElement()
    ink.run()
    win = ImageWithLineWindow(ink.fileName, ink.arrows, "objets_isoles.jpg") 


