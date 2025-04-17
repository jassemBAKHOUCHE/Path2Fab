import inkex
from inkex import EffectExtension, ShapeElement

class AfficherElementsSelectionnes(EffectExtension):
    def effect(self):
        selection = self.svg.selection

        if not selection:
            inkex.errormsg("Aucun élément sélectionné.")
            return

        for element in selection:
            if isinstance(element, ShapeElement):
                element.style['fill'] = 'none'

                element.style['stroke'] = '#000000'  
                element.style['stroke-width'] = '1px'  

              
if __name__ == '__main__':
    AfficherElementsSelectionnes().run()