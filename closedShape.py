import inkex
import re

class ClosedShape(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument('--exclude_layers', type=str, default="layer1,svg1,namedview1,defs1", help="Liste des objets à exclure séparés par des virgules")

    def effect(self):
        for element in self.document.getroot().iter():
            element_id = element.get_id()
            # check if the element is a path and if its border is black
            if re.search("^path.*$", element_id) and (element.style.get_color(name='stroke').red == 0 and element.style.get_color(name='stroke').blue == 0 and element.style.get_color(name='stroke').red == 0):
                path = element.get_path()

                if re.search("^.*[zZ]$", str(path)): # closed path
                    text = "closed"
                else : text = "opened"
                self.msg(f"{element_id} is {text}\n")

         
if __name__ == '__main__':
    ClosedShape().run()
