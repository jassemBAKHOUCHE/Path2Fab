import inkex
import re
import os
import subprocess
from pathlib import Path

class SaveExtension(inkex.EffectExtension):
    def add_arguments(self, pars):
        pars.add_argument("--filename", type=str, default="", help="Nom du fichier")
        pars.add_argument("--export_pdf", type=inkex.Boolean, default=False, help="Exporter en PDF")
        pars.add_argument("--export_dxf", type=inkex.Boolean, default=False, help="Exporter en DXF")
        pars.add_argument("--export_svg", type=inkex.Boolean, default=False, help="Exporter en SVG")
    
    def effect(self):
        if not re.match(r'^[a-zA-Z0-9\-]+$', self.options.filename, re.IGNORECASE):
            inkex.errormsg("Le nom du fichier contient des caractères non autorisés. Utilisez uniquement a-z, 0-9 et -.")
            return
        
        downloads_folder = str(Path.home() / "Downloads")

        if not os.path.exists(downloads_folder):
            inkex.errormsg(f"Le dossier 'Téléchargements' n'existe pas : {downloads_folder}")
            return
        
        base_filepath = os.path.join(downloads_folder, self.options.filename)
        

        exports = []
        try:
            if self.options.export_svg:
                svg_path = base_filepath + ".svg"
                self.document.write(svg_path)
                exports.append("SVG")
            
            if self.options.export_pdf:
                pdf_path = base_filepath + ".pdf"
                self.export_with_inkscape(svg_path if self.options.export_svg else None, pdf_path, "pdf")
                exports.append("PDF")
            
            if self.options.export_dxf:
                dxf_path = base_filepath + ".dxf"
                self.export_with_inkscape(svg_path if self.options.export_svg else None, dxf_path, "dxf")
                exports.append("DXF")
        
        except Exception as e:
            inkex.errormsg(f"Une erreur s'est produite lors de l'enregistrement des fichiers : {e}")
            return
        
        export_message = ", ".join(exports) if exports else "Aucun format sélectionné"
        inkex.errormsg(f"Fichiers enregistrés dans {downloads_folder}\nFormats sélectionnés : {export_message}")
    
    def export_with_inkscape(self, input_path, output_path, export_format):
        """
        Utilise Inkscape en ligne de commande pour exporter un fichier SVG vers un autre format.
        Si input_path est None, utilise le document actuel.
        """
        try:

            if input_path is None:
                temp_svg_path = os.path.join(os.path.expanduser("~"), "temp_export.svg")
                self.document.write(temp_svg_path)
                input_path = temp_svg_path
            
            command = [
                "inkscape",
                input_path,
                f"--export-filename={output_path}",
                f"--export-type={export_format}"
            ]
            
            subprocess.run(command, check=True)
        
        except subprocess.CalledProcessError as e:
            inkex.errormsg(f"Erreur lors de l'export {export_format.upper()} : {e}")
        except Exception as e:
            inkex.errormsg(f"Erreur inattendue lors de l'export {export_format.upper()} : {e}")
        finally:
            if input_path is not None and "temp_export.svg" in input_path:
                os.remove(input_path)

if __name__ == "__main__":
    SaveExtension().run()