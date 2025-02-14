import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, Gdk

class HelpWindow(Gtk.Window):
    def __init__(self):
        super().__init__(title="Aide Laser Cut")
        self.set_border_width(10)
        self.set_default_size(300, 150)

        # Création d'une boîte verticale pour les lignes
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=5)
        self.add(vbox)

    def add_row(self, container, text, color):
        # Conteneur pour chaque ligne
        hbox = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=10)
        container.pack_start(hbox, False, False, 0)

        # Ajout du trait coloré
        color_box = Gtk.Box()
        color_box.set_size_request(20, 10)  # Taille du trait
        color_box.override_background_color(Gtk.StateFlags.NORMAL, color)
        hbox.pack_start(color_box, False, False, 0)

        # Ajout du texte explicatif
        label = Gtk.Label(label=text)
        hbox.pack_start(label, False, False, 0)

if __name__ == "__main__":
    win = HelpWindow()
    win.connect("destroy", Gtk.main_quit)
    win.show_all()
    Gtk.main()
