import inkex

class UngroupAll(inkex.EffectExtension):
    def effect(self):
        self.ungroup_all(self.document.getroot())

    def ungroup_all(self, parent):
        # Copie de la liste des enfants pour éviter les modifications pendant l'itération
        for elem in list(parent):
            self.ungroup_all(elem)

            if isinstance(elem, inkex.Group):
                index = parent.index(elem)
                for child in list(elem):
                    parent.insert(index, child)
                    index += 1
                # Supprime le groupe
                parent.remove(elem)

if __name__ == '__main__':
    UngroupAll().run()
