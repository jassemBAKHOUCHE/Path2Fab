
import inkex
import sys

class TooSmallObject(inkex.EffectExtension):
    def effect(self):
        limit_size = 1.0  # mm
        tab_paths = []

        for elem in self.document.getroot().iter():
            if isinstance(elem, inkex.ShapeElement):
                try:
                    bbox = elem.bounding_box()
                    width, height = bbox.width, bbox.height
                    if width < limit_size or height < limit_size:
                        tab_paths.append(elem.get_id())
                except Exception as e:
                    # self.msg(elem.get_id())-> donne Layer 1 qui n'est pas un path. 
                    # le bug etait dans le elem.bounding_box() qui n'etait pas defini sur
                    # certains elements, dans mon cas le Layer (la page blanche principale).
                    # donc on gere ça avec une Exception
                    continue

        if not tab_paths:
            sys.stderr.write("Aucun élément n'est trop petit pour la découpeuse laser.\n")
        else:
            paths_str = ", ".join(tab_paths)
            sys.stderr.write(
                f"Les éléments suivants sont trop petits pour la découpeuse laser.\n"
                f"Leurs largeur ou hauteur sont inférieures à {limit_size} mm.\n"
                f"Éléments impliqués : {paths_str}\n"
                f"Vous pouvez les localiser dans les calques de votre projet.\n"
            )

if __name__ == '__main__':
    TooSmallObject().run()
