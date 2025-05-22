from PIL import Image, ImageDraw
import cairosvg

### DRAW ARROWS ###
class ImageWithLineWindow:
    def __init__(self, SVGFile, arrowsTab, nameImage):
        # Convert SVG to PNG using CairoSVG
        cairosvg.svg2png(url=SVGFile, write_to="tmp.png")

        # Open the converted image
        pil_image = Image.open("tmp.png").convert("RGBA")
        
        factor = 3.75
        
        for i in range(len(arrowsTab)):
            for j in range(len(arrowsTab[i])):
                arrowsTab[i][j] *= factor

        for arrow in arrowsTab:
            self.draw_line_on_pil_image(
                pil_image,
                arrow[0], arrow[1], arrow[2], arrow[3],
                arrow[4], arrow[5], arrow[6], arrow[7]
            )

        if arrowsTab:
            # Create a white background
            new_image = Image.new("RGBA", pil_image.size, "WHITE")
            new_image.paste(pil_image, (0, 0), pil_image)
            new_image.convert("RGB").save(nameImage, "JPEG")

            img = Image.open(nameImage)
            img.show()

    def draw_line_on_pil_image(self, pil_image, center_x, center_y, start_x, start_y, left_x, left_y, right_x, right_y):
        draw = ImageDraw.Draw(pil_image)
        draw.line([(start_x, start_y), (center_x, center_y)], fill="red", width=2)
        draw.line([(left_x, left_y), (center_x, center_y)], fill="red", width=2)
        draw.line([(right_x, right_y), (center_x, center_y)], fill="red", width=2)
