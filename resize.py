import inkex
class ResizePage(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--preset', type=str, default='custom', help='Présélection de la taille de la page')
        pars.add_argument('--width', type=float, default=210.0, help='Largeur de la page en mm')
        pars.add_argument('--height', type=float, default=297.0, help='Hauteur de la page en mm')

    def effect(self):
        """Modifie la taille de la page SVG selon le préréglage ou les dimensions personnalisées."""
        presets = {
            'a4': (210.0, 297.0),
            'a3': (297.0, 420.0),
            'letter': (216.0, 279.0),
            'square': (200.0, 200.0),
        }

        #Tester
        if self.options.preset in presets:
            self.options.width, self.options.height = presets[self.options.preset]

        #Recuperer
        width_px = self.options.width
        height_px = self.options.height

        #Appliquer 
        self.svg.set('width', f"{self.options.width}mm")
        self.svg.set('height', f"{self.options.height}mm")
        self.svg.set('viewBox', f"0 0 {width_px} {height_px}")

if __name__ == '__main__':
    ResizePage().run()
