import inkex
from inkex import TextElement, PathElement

class CheckColor(inkex.EffectExtension):
    def effect(self):
        selection = self.svg.selection

        if not selection:
            inkex.errormsg("Aucun élément sélectionné.")
            return

        for element in selection:
            if  element.style['stroke'] != '#000000' or element.style['stroke'] != '#00FF00' or element.style['stroke'] != '#0000FF' :
                inkex.utils.debug(f"L'élément {element.get_id()} n'est pas de la bonne couleur.")

if __name__ == "__main__":
    CheckColor().run()