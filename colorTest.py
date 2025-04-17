import TextElement, PathElement

class ColorTest(inkex.EffectExtension):
    def effect(self):
        selection = self.svg.selection

        if not selection:
            inkex.errormsg("Aucun élément sélectionné.")
            return

        allowed_colors = ['#000000', '#00ff00', '#0000ff']

        for element in selection:
            stroke_color = element.style.get('stroke', None)
            if stroke_color not in allowed_colors:
                inkex.utils.debug(f"L'élément {element.get_id()} n'est pas de la bonne couleur (stroke={stroke_color}).")
            else :
                inkex.utils.debug(f"L'élément {element.get_id()} est pas de la bonne couleur (stroke={stroke_color}).")



if __name__ == "__main__":
    ColorTest().run()
