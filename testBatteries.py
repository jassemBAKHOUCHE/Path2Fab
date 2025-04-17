import inkex
from inkex.localization import inkex_gettext as _

# Import des autres extensions (elles doivent être dans le même dossier)
from vectorText import VectorText
from closedShape import ClosedShape
from bezierIntersect import BezierIntersect
from lineIntersect import LineIntersect
from colorTest import ColorTest
from isolatedElement import IsolatedElement
from polygonIntersect import PolygonIntersect
from tooSmallObject import TooSmallObject

class TestBatteries(inkex.EffectExtension):
    def add_arguments(self, parser):
        parser.add_argument("--vectorText", type=inkex.Boolean, default=False,
                            help="Lancer Vector Text")
        parser.add_argument("--closedShape", type=inkex.Boolean, default=False,
                            help="Lancer Closed Shape")
        parser.add_argument("--bezierIntersect", type=inkex.Boolean, default=False,
                            help="Lancer Bezier Intersect")
        parser.add_argument("--lineIntersect", type=inkex.Boolean, default=False,
                            help="Lancer Line intersect")
        parser.add_argument("--colorTest", type=inkex.Boolean, default=False,
                            help="Lancer Color test")
        parser.add_argument("--isolatedElement", type=inkex.Boolean, default=False,
                            help="Lancer isolated Element")
        parser.add_argument("--polygonIntersect", type=inkex.Boolean, default=False,
                            help="Lancer polygon intersect")       
        parser.add_argument("--tooSmallObject", type=inkex.Boolean, default=False,
                            help="Lancer too small object")                      

    def effect(self):
        if not any([
            self.options.vectorText,
            self.options.closedShape,
            self.options.bezierIntersect,
            self.options.lineIntersect,
            self.options.colorTest,
            self.options.isolatedElement,
            self.options.polygonIntersect,
            self.options.tooSmallObject,
        ]):
            inkex.errormsg(_("Aucune extension sélectionnée."))
            return

        # Dictionnaire des extensions disponibles
        extensions = {
            'vectorText': VectorText,
            'closedShape': ClosedShape,
            'bezierIntersect': BezierIntersect,
            'lineIntersect': LineIntersect,
            'colorTest': ColorTest,
            'isolatedElement': IsolatedElement,
            'polygonIntersect': PolygonIntersect,
            'tooSmallObject': TooSmallObject
        }

        for ext_name, ext_class in extensions.items():
            if getattr(self.options, ext_name):
                try:
                    instance = ext_class()
                    instance.document = self.document  # Partage du même document
                    instance.svg = self.svg            # Nécessaire pour manipuler les éléments SVG
                    instance.options = self.options    # Partage des mêmes options si besoin
                    instance.effect()                  # Appelle la logique de l'extension

                    inkex.utils.debug(f"Extension '{ext_name}' lancée avec succès.")
                except Exception as e:
                    inkex.errormsg(f"Erreur lors du lancement de '{ext_name}': {str(e)}")

if __name__ == '__main__':
    TestBatteries().run()
