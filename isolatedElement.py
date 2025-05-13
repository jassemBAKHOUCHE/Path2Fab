
import inkex
import math
import sys
import warnings
warnings.filterwarnings("ignore", category=ResourceWarning)

def distance(a, b):
    xa, ya = a
    xb, yb = b
    return math.hypot(xb - xa, yb - ya)

class IsolatedElement(inkex.EffectExtension):
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
                center = (bbox.center_x, bbox.center_y)
                elements.append((elem.get_id(), center, bbox))

                # Check if it's outside the page boundaries
                if (bbox.right < page_left or bbox.left > page_right or
                    bbox.bottom < page_top or bbox.top > page_bottom):
                    off_page_ids.append(elem.get_id())
            except Exception:
                continue

        if len(elements) < 2:
            sys.stderr.write("Pas assez d'éléments pour détecter un isolement.\n")
        else:
            max_dist = -1
            most_isolated_id = None

            for i, (id1, c1, _) in enumerate(elements):
                min_neighbor_dist = math.inf
                for j, (id2, c2, _) in enumerate(elements):
                    if id1 == id2:
                        continue
                    d = distance(c1, c2)
                    if d < min_neighbor_dist:
                        min_neighbor_dist = d
                if min_neighbor_dist > max_dist:
                    max_dist = min_neighbor_dist
                    most_isolated_id = id1

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

if __name__ == '__main__':
    IsolatedElement().run()
