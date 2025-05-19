import math
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'libs'))
import inkex

class ColorTest(inkex.EffectExtension):
    def __init__(self):
        super().__init__()
        self.fileName = self.document_path()
        self.arrows = []

    def effect(self):
        selection = self.svg.selection

        if not selection:
            inkex.errormsg("Aucun élément sélectionné.")
            return

        allowed_colors = ['#000000', "#ff0000", '#0000ff']

        for element in selection:
            stroke_color = element.style.get('stroke', None)
            if stroke_color not in allowed_colors:
                arrow_size = 5
                # the bounding box 
                bbox = element.bounding_box()

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

                inkex.utils.debug(f"L'élément {element.get_id()} n'est pas de la bonne couleur (stroke={stroke_color}).")
            else :
                inkex.utils.debug(f"L'élément {element.get_id()} est pas de la bonne couleur (stroke={stroke_color}).")
        self.msg(f"COULEURS LASER VALIDES : Nombre d'erreur(s) trouvée(s) : {len(self.arrows)}\n\n")


if __name__ == "__main__":
    ColorTest().run()
