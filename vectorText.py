import math
import os, webbrowser
import inkex
import numpy as np
from PIL import Image, ImageDraw
from inkex import TextElement
import cairosvg
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

class VectorText(inkex.EffectExtension):
    def __init__(self):
        super().__init__()
        self.svg = os.path.join(self.svg_path(), self.name)
        self.fileName = self.document_path()
        self.arrows = []

    def effect(self):
        for element in self.svg.iter():
            if isinstance(element, TextElement):
                # Add in the array for each element the position of the arrow
                # Must use get_inkscape_bbox() when it comes to text elements
                bbox = element.get_inkscape_bbox()

                if bbox:
                    # Get coordinates for the rectangle 
                    left_x = bbox.top - 5
                    right_x = left_x + bbox.height + 10
                    top_y = bbox.left - 5 
                    bottom_y = top_y + bbox.width + 10           

                    self.arrows.append([left_x, right_x, top_y, bottom_y])
        self.msg(f"TEXTE VECTORISE : Nombre d'erreur(s) trouvée(s): {len(self.arrows)}\n\n")
                

### DRAW RECTANGLE ###
class ImageWithRectWindow:
    def __init__(self, SVGFile, arrowsTab, nameImage):
        # Convert SVG to PNG using CairoSVG
        cairosvg.svg2png(url=SVGFile, write_to="tmp.png")

        # Open the converted image
        pil_image = Image.open("tmp.png").convert("RGBA")
        
        factor = 3.75
        
        for i in range(len(arrowsTab)):
            for j in range(len(arrowsTab[i])):
                arrowsTab[i][j] *= factor

        for arrow in arrowsTab:
            self.draw_line_on_pil_image(
                pil_image,
                arrow[0], arrow[1], arrow[2], arrow[3]
            )

        if arrowsTab:
            # Create a white background
            new_image = Image.new("RGBA", pil_image.size, "WHITE")
            new_image.paste(pil_image, (0, 0), pil_image)
            new_image.convert("RGB").save(nameImage, "JPEG")

            img = Image.open(nameImage)
            img.show()

    def draw_line_on_pil_image(self, pil_image,  top_y, bottom_y, left_x, right_x):
        """Draw a red rectangle on the Pillow image."""
        draw = ImageDraw.Draw(pil_image)
        draw.line([(left_x, top_y), (right_x, top_y)], fill="red", width=2)
        draw.line([(left_x, bottom_y), (right_x, bottom_y)], fill="red", width=2)
        draw.line([(left_x, top_y), (left_x, bottom_y)], fill="red", width=2)
        draw.line([(right_x, top_y), (right_x, bottom_y)], fill="red", width=2)
        

if __name__ == "__main__":
    ink = VectorText()
    ink.run()
    win = ImageWithRectWindow(ink.fileName, ink.arrows, "texte_vectorise.jpg") 
