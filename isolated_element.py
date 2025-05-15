
import inkex
import math
import sys
import numpy as np
from PIL import Image, ImageDraw
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, GdkPixbuf
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

def distance(a, b):
    xa, ya = a
    xb, yb = b
    return math.hypot(xb - xa, yb - ya)

class IsolatedElement(inkex.EffectExtension):
    def __init__(self):
        super().__init__()
        self.fileName = self.document_path()
        self.arrows = []

    def add_arguments(self, pars):
        #pars.add_argument('--exclude_layers', type=str, default="layer1,svg1,namedview1,defs1", help="IDs à ignorer")
        pass

    def effect(self):
        exclude = {"layer1", "svg1", "namedview1", "defs1"}

        
        svg_width = self.svg.unittouu(self.svg.attrib.get('width'))
        svg_height = self.svg.unittouu(self.svg.attrib.get('height'))

        page_left = 0
        page_right = svg_width
        page_top = 0
        page_bottom = svg_height
        elements = []
        off_page_ids = []

        for elem in self.document.getroot().iter():
            if not elem.get_id() or elem.get_id() in exclude:
                continue
            if not isinstance(elem, inkex.ShapeElement):
                continue
            try:
                bbox = elem.bounding_box()
                arrow_size = 5
                center = (bbox.center_x, bbox.center_y)
                # Get coordinates for the arrow 
                start_x = (bbox.left + bbox.right) / 2
                start_y = (bbox.top + bbox.bottom) / 2
                center_x, center_y = bbox.left, bbox.top  
                    
                angle = math.atan2(center_y - start_y, center_x - start_x)
                left_x = center_x - arrow_size * math.cos(angle - math.pi / 6)
                left_y = center_y - arrow_size * math.sin(angle - math.pi / 6)
                right_x = center_x - arrow_size * math.cos(angle + math.pi / 6)
                right_y = center_y - arrow_size * math.sin(angle + math.pi / 6)


                elements.append((elem.get_id(), center, bbox, [start_x, start_y, center_x, center_y, left_x, left_y, right_x, right_y]))

                # Check if it's outside the page boundaries
                if (bbox.right < page_left or bbox.left > page_right or
                    bbox.bottom < page_top or bbox.top > page_bottom):
                    off_page_ids.append(elem.get_id())
                    self.arrows.append([start_x, start_y, center_x, center_y, left_x, left_y, right_x, right_y])
            except Exception:
                continue

        if len(elements) < 2:
            sys.stderr.write("Pas assez d'éléments pour détecter un isolement.\n")
        else:
            max_dist = -1
            most_isolated_id = None
            ind = -1

            for i, (id1, c1, _, _) in enumerate(elements):
                min_neighbor_dist = math.inf
                for j, (id2, c2, _, _) in enumerate(elements):
                    if id1 == id2:
                        continue
                    d = distance(c1, c2)
                    if d < min_neighbor_dist:
                        min_neighbor_dist = d
                if min_neighbor_dist > max_dist:
                    max_dist = min_neighbor_dist
                    most_isolated_id = id1
                    ind = i

            self.arrows.append(elements[ind][3])
            self.msg(f"arrows tab : {self.arrows}")
            
            dist_mm = self.svg.uutounit(max_dist, 'mm')
            sys.stderr.write(f"L'élément le plus isolé est : {most_isolated_id}, à {dist_mm:.2f} mm de son plus proche voisin.\n")
            self.svg.selection.add(most_isolated_id)

        if off_page_ids:
            ids = ", ".join(off_page_ids)
            sys.stderr.write(f"Les éléments suivants sont hors de la page : {ids}\n")
            for eid in off_page_ids:
                self.svg.selection.add(eid)
        else:
            sys.stderr.write("Aucun élément n'est hors de la page.\n")
        
        self.msg(f"Nombre d'erreur(s) trouvée(s): {len(self.arrows)}\n\n")




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
    ink = IsolatedElement()
    ink.run()
    win = ImageWithLineWindow(ink.fileName, ink.arrows) 
    

