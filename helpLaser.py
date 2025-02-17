import gi
import math
import inkex

gi.require_version("Gtk", "3.0")
from gi.repository import Gtk, cairo


class FindShapesCenter(inkex.EffectExtension):
    def effect(self):
        shapes = []

        for element in self.svg.iter():
            element_id = element.get_id()


            if isinstance(element, (inkex.PathElement, inkex.Rectangle, inkex.Circle, inkex.Ellipse, inkex.Polygon)):
                bbox = element.bounding_box()
                if bbox:
                    center_x = (bbox.left + bbox.right) / 2
                    center_y = (bbox.top + bbox.bottom) / 2
                    shapes.append((element, center_x, center_y, element_id))

        if shapes:
            win = ShapeWindow(shapes)
            win.connect("destroy", Gtk.main_quit)
            win.show_all()
            Gtk.main()


class ShapeDrawing(Gtk.DrawingArea):
    def __init__(self, shapes):
        super().__init__()
        self.shapes = shapes
        self.connect("draw", self.on_draw)

    def on_draw(self, widget, cr):
        for shape, center_x, center_y, element_id in self.shapes:
            self.draw_shape(cr, shape)
            # changer le code ici s'il faut que certaines formes
            self.draw_arrow(cr, shape, center_x, center_y)

        cr.stroke()

    def draw_shape(self, cr, shape):
        cr.set_source_rgb(0.5, 0.5, 0.5)
        bbox = shape.bounding_box()
        if isinstance(shape, inkex.Rectangle):
            cr.rectangle(bbox.left, bbox.top, bbox.width, bbox.height)
        elif isinstance(shape, inkex.Circle):
            cr.arc(bbox.center_x, bbox.center_y, bbox.width / 2, 0, 2 * math.pi)
        elif isinstance(shape, inkex.Ellipse):
            cr.save()
            cr.translate(bbox.center_x, bbox.center_y)
            cr.scale(bbox.width / 2, bbox.height / 2)
            cr.arc(0, 0, 1, 0, 2 * math.pi)
            cr.restore()
        elif isinstance(shape, inkex.Polygon):
            points = [(p.real, p.imag) for p in shape.points]
            cr.move_to(*points[0])
            for point in points[1:]:
                cr.line_to(*point)
            cr.close_path()
        cr.fill()

    def draw_arrow(self, cr, shape, center_x, center_y, arrow_size=10):
        cr.set_source_rgb(1, 0, 0)
        cr.set_line_width(2)
        bbox = shape.bounding_box()
        start_x, start_y = bbox.left, bbox.top  # Départ en haut à gauche
        cr.move_to(start_x, start_y)
        cr.line_to(center_x, center_y)
        cr.stroke()
        angle = math.atan2(center_y - start_y, center_x - start_x)
        left_x = center_x - arrow_size * math.cos(angle - math.pi / 6)
        left_y = center_y - arrow_size * math.sin(angle - math.pi / 6)
        right_x = center_x - arrow_size * math.cos(angle + math.pi / 6)
        right_y = center_y - arrow_size * math.sin(angle + math.pi / 6)
        cr.move_to(center_x, center_y)
        cr.line_to(left_x, left_y)
        cr.move_to(center_x, center_y)
        cr.line_to(right_x, right_y)
        cr.stroke()


class ShapeWindow(Gtk.Window):
    def __init__(self, shapes):
        super().__init__(title="Affichage des formes avec flèches")
        self.set_default_size(800, 600)
        drawing_area = ShapeDrawing(shapes)
        self.add(drawing_area)


if __name__ == "__main__":
    FindShapesCenter().run()
