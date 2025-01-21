"""
Une extension Inkscape minimale qui ne fait rien de particulier.
"""

import inkex

class MinimalExtension(inkex.EffectExtension):

    def effect(self):
        """
        Point d'entrée principal de l'extension.
        Actuellement, cette extension ne fait rien.
        """
        inkex.utils.debug("Extension exécutée avec succès, mais aucune action n'a été effectuée.")

if __name__ == "__main__":
    MinimalExtension().run()