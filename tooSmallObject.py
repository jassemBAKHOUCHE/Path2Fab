
import math
import inkex
import sys
from inkex import Transform
from drawArrow import ImageWithLineWindow
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)


class TooSmallObject(inkex.EffectExtension):
    def __init__(self):
        super().__init__()
        self.fileName = self.document_path()
        self.arrows = []

    def effect(self):
        limit_size = 1
        tab_paths = []

        for elem in self.document.getroot().iter():
            # check if the element if a graphic form
            if isinstance(elem, inkex.ShapeElement) and not isinstance(elem, inkex.elements._groups.Layer):

                try : 
                    # stroke color 
                    color = elem.style.get('stroke', None)
                    if color == '#ff0000': # detect only when it's for cutting 
                        # the bounding box 
                        bbox = elem.bounding_box()

                        # keep the center to translate the object after to put the object just as before transformations 
                        centerX_before = bbox.center_x
                        centerY_before = bbox.center_y

                        # rotate the object to know if it's a too small object rotated 
                        for degree in range(0, 91):
                            
                            # rotate the object 
                            rotate_transform = Transform()
                            rotate_transform.add_rotate(1, bbox.center) 
                            elem.transform = elem.transform @ rotate_transform
                            bbox = elem.bounding_box() 

                            # dimensions
                            width, height = bbox.width, bbox.height

                            if (width < limit_size or height < limit_size) : 
                                tab_paths.append(elem.get_id())
                                self.svg.selection.add(elem.get_id())

                                arrow_size = 5

                                if bbox:
                                    
                                    center_x, center_y = bbox.left, bbox.top 
                                    start_x = center_x + 5
                                    start_y =  center_y + 5
                                    
                                    angle = math.atan2(center_y - start_y, center_x - start_x)
                                    left_x = center_x - arrow_size * math.cos(angle - math.pi / 6)
                                    left_y = center_y - arrow_size * math.sin(angle - math.pi / 6)
                                    right_x = center_x - arrow_size * math.cos(angle + math.pi / 6)
                                    right_y = center_y - arrow_size * math.sin(angle + math.pi / 6)

                                    self.arrows.append([start_x, start_y, center_x, center_y, left_x, left_y, right_x, right_y])

                                break
                        
                        # rotate to put the object in the good way 
                        rotate_transform = Transform()
                        rotate_transform.add_rotate(-degree-1, bbox.center)
                        elem.transform = elem.transform @ rotate_transform
                        
                        # translate the object after rotation
                        bbox = elem.bounding_box()
                        centerX_after = bbox.center_x
                        centerY_after = bbox.center_y
                        translate_transform = Transform()
                        translate_transform.add_translate(-(centerX_after - centerX_before), -(centerY_after - centerY_before))
                        elem.transform = elem.transform @ translate_transform

                except Exception as e:
                    continue

        # create a good print 
        if len(tab_paths) == 0:
            sys.stderr.write('Auncun élément est trop petit pour la découpeuse laser')
        else :
            if tab_paths[0]:
                paths = tab_paths[0]
            for i in range(1, len(tab_paths)) :
                paths += ", " + tab_paths[i]
            sys.stderr.write(f'Les éléments suivants sont trop petits pour la découpeuse laser.\nLeur longueur et leur largeur doivent être inférieures à {limit_size} mm pour être acceptées\nEléments impliqués : {paths}\nVous pouvez trouver ces éléments dans les calques de votre projet.\n')
        
        self.msg(f"OBJETS TROP PETITS : Nombre d'erreur(s) trouvée(s): {len(self.arrows)}\n\n")


if __name__ == '__main__':
    ink =  TooSmallObject()
    ink.run()
    win = ImageWithLineWindow(ink.fileName, ink.arrows, "objets_petits.jpg") 

