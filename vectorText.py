import math
import os, webbrowser
import gi
import inkex
import numpy as np
from PIL import Image, ImageDraw
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
from inkex import TextElement
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
                

### DRAW ARROWS ###
class ImageWithRectWindow(Gtk.Window):
    def __init__(self, SVGFile, arrowsTab):
        # Load the SVG into a GdkPixbuf
        self.pixbuf = GdkPixbuf.Pixbuf.new_from_file(SVGFile)

        # Convert GdkPixbuf to Pillow Image
        pil_image = self.gdkpixbuf_to_pil(self.pixbuf)

        factor = 3.55
        # Update arrow position
        for i in range(len(arrowsTab)) :
            for j in range(len(arrowsTab[i])) :
                arrowsTab[i][j] = arrowsTab[i][j]*factor


        # Draw on the Pillow image
        for arrow in arrowsTab :
            self.draw_line_on_pil_image(pil_image, arrow[0], arrow[1], arrow[2], arrow[3])
        if len(arrowsTab) > 0:
            # Convert the Pillow image back to GdkPixbuf
            self.pixbuf = self.pil_to_gdkpixbuf(pil_image)

            # Save the buffer into an image
            self.pixbuf.savev('tmp.png', 'png')                

            image = Image.open('tmp.png')
            # Create a white background
            new_image = Image.new("RGBA", image.size, "WHITE") 
            # Paste the image on the background
            new_image.paste(image, (0, 0), image)  
            # Save as JPEG            
            new_image.convert('RGB').save('text_vectorise.jpg', "JPEG") 
            # Display the image
            img = Image.open("text_vectorise.jpg")
            img.show()


    def gdkpixbuf_to_pil(self, pixbuf):
        """Convert a GdkPixbuf to a Pillow Image."""
        width = pixbuf.get_width()
        height = pixbuf.get_height()
        pixels = np.ndarray(
            (height, width, 4), dtype=np.uint8,
            buffer=pixbuf.get_pixels())
        pil_image = Image.fromarray(pixels, 'RGBA')
        return pil_image

    def pil_to_gdkpixbuf(self, pil_image):
        """Convert a Pillow Image back to a GdkPixbuf."""
        pil_image = pil_image.convert('RGBA')
        width, height = pil_image.size
        data = np.array(pil_image)
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(
            data.tobytes(), GdkPixbuf.Colorspace.RGB, True, 8, width, height,
            width * 4)
        return pixbuf

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
    win = ImageWithRectWindow(ink.fileName, ink.arrows) 
