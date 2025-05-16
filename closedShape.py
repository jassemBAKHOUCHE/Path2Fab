import math
import os
import inkex
from drawArrow import ImageWithLineWindow
import re
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

class ClosedShape(inkex.EffectExtension):
    def __init__(self):
        super().__init__()
        self.svg = os.path.join(self.svg_path(), self.name)
        self.fileName = self.document_path()
        self.arrows = []

    def effect(self):
        tabelement = []
        for element in self.document.getroot().iter():

            # Test line color and type
            if isinstance(element, inkex.PathElement) and (element.style.get_color(name='stroke').red == 0 and element.style.get_color(name='stroke').blue == 255 and element.style.get_color(name='stroke').green == 0):
                tabelement.append(element)
                path = element.get_path()

                # svg indication for closed paths
                if re.search("^.*[zZ]$", str(path)): continue

                # Mark on wich elements should the arrow(s) be
                bbox = element.bounding_box()
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

        # Indication about number of errors
        self.msg(f"FORMES FERMEES : Nombre d'erreur(s) trouvée(s) : {len(self.arrows)}\n\n")

if __name__ == '__main__':
    ink = ClosedShape()
    ink.run()
    win = ImageWithLineWindow(ink.fileName, ink.arrows, "formes_fermees.jpg") 
