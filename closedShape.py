import math
import os
import gi
import inkex
import numpy as np
from PIL import Image, ImageDraw
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk, GdkPixbuf
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
                    start_x = (bbox.left + bbox.right) / 2
                    start_y = (bbox.top + bbox.bottom) / 2

                    center_x, center_y = bbox.left, bbox.top  
                    
                    angle = math.atan2(center_y - start_y, center_x - start_x)
                    left_x = center_x - arrow_size * math.cos(angle - math.pi / 6)
                    left_y = center_y - arrow_size * math.sin(angle - math.pi / 6)
                    right_x = center_x - arrow_size * math.cos(angle + math.pi / 6)
                    right_y = center_y - arrow_size * math.sin(angle + math.pi / 6)

                    self.arrows.append([start_x, start_y, center_x, center_y, left_x, left_y, right_x, right_y])

        # Indication about number of errors
        self.msg(f"FORMES FERMEES : Nombre d'erreur(s) trouvée(s) : {len(self.arrows)}\n\n")

### DRAW ARROWS ###
class ImageWithLineWindow(Gtk.Window):
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
            self.draw_line_on_pil_image(pil_image, arrow[0], arrow[1], arrow[2], arrow[3], arrow[4], arrow[5], arrow[6], arrow[7])
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
        new_image.convert('RGB').save('formes_fermees.jpg', "JPEG") 
        # Display the image
        img = Image.open("formes_fermees.jpg")
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

    def draw_line_on_pil_image(self, pil_image,  center_x, center_y, start_x, start_y, left_x, left_y, right_x, right_y):
        """Draw a red line on the pillow image."""
        draw = ImageDraw.Draw(pil_image)
        draw.line([(start_x, start_y), (center_x, center_y)], fill="red", width=2)
        draw.line([(left_x, left_y), (center_x, center_y)], fill="red", width=2)
        draw.line([(right_x, right_y), (center_x, center_y)], fill="red", width=2)         

if __name__ == '__main__':
    ink = ClosedShape()
    ink.run()
    win = ImageWithLineWindow(ink.fileName, ink.arrows) 
