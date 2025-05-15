
import inkex
import sys
from inkex import Transform

class TooSmallObject(inkex.EffectExtension):
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
            sys.stderr.write(f'Les éléments suivants sont trop petits pour la découpeuse laser.\nLeurs longeur et largeur doivent être inférieur à {limit_size} mm sans contour pour être acceptés.\nEléments impliqués : {paths}\nVous pouvez trouver ces éléments dans les calques de votre projet.')

if __name__ == '__main__':
    TooSmallObject().run()
