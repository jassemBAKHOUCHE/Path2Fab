import inkex
from inkex import EffectExtension, ShapeElement

class AfficherElementsSelectionnes(EffectExtension):
    def effect(self):
        # Récupérer les éléments sélectionnés
        selection = self.svg.selection

        if not selection:
            inkex.errormsg("Aucun élément sélectionné.")
            return

        # Parcourir les éléments sélectionnés
        for element in selection:
            if isinstance(element, ShapeElement):
                # Enlever le fond (remplissage)
                # element.style['fill'] = '#000000'
                element.style['fill'] = 'none'
                
                # Mettre le contour en noir
                element.style['stroke'] = '#000000'  
                element.style['stroke-width'] = '1px'  

              
if __name__ == '__main__':
    AfficherElementsSelectionnes().run()