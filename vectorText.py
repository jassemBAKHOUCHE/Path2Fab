import inkex
from inkex import TextElement, PathElement

class VectorText(inkex.EffectExtension):
    def effect(self):

        for elem in self.svg.iter():
            if isinstance(elem, TextElement):
                inkex.utils.debug(f"L'élément {elem.get_id()} est un texte non vectorisé.")
            elif isinstance(elem, PathElement):
                # Vérifier si le chemin provient d'un texte vectorisé
                if elem.get("inkscape:original-text", None) is not None:
                    inkex.utils.debug(f"L'élément {elem.get_id()} est un texte vectorisé.")
                else:
                    inkex.utils.debug(f"L'élément {elem.get_id()} est un chemin, mais pas un texte vectorisé.")

if __name__ == "__main__":
    VectorText().run()