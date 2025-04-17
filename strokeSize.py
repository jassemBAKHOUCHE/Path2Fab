import inkex

class StrokeSize(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--stroke_width_mm", type=float, default=0.2, help="Nouvelle épaisseur du contour (en mm)")

    def effect(self):
        if not self.svg.selected:
            inkex.errormsg("Aucun objet sélectionné.")
            return

        stroke_width_px = self.options.stroke_width_mm * 3.543307

        for elem in self.svg.selection:
            elem.style['stroke-width'] = str(stroke_width_px)

StrokeSize().run()
