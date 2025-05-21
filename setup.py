import os
import sys
import platform
import subprocess
import shutil
import xml.etree.ElementTree as ET

# === 1. Détection OS & chemins ===
home = os.path.expanduser("~")
venv_dir = os.path.join(home, ".inkscapepythonenv")

if platform.system() == "Windows":
    python_bin = os.path.join(venv_dir, "Scripts", "python.exe")
    pip_bin = os.path.join(venv_dir, "Scripts", "pip.exe")
    config_path = os.path.join(os.environ["APPDATA"], "inkscape", "preferences.xml")
    extensions_dir = os.path.join(os.environ["APPDATA"], "inkscape", "extensions")
else:
    python_bin = os.path.join(venv_dir, "bin", "python3.13")
    pip_bin = os.path.join(venv_dir, "bin", "pip")
    config_path = os.path.join(home, ".config", "inkscape", "preferences.xml")
    extensions_dir = os.path.join(home, ".config", "inkscape", "extensions")

requirements_file = os.path.join(os.path.dirname(__file__), "libs.txt")

# === 2. Création du venv ===
if not os.path.exists(python_bin):
    print(f"[INFO] Création du venv dans : {venv_dir}")
    try:
        subprocess.check_call([sys.executable, "-m", "venv", venv_dir])
    except subprocess.CalledProcessError:
        print("[ERREUR] Échec de création du venv", file=sys.stderr)
        sys.exit(1)
else:
    print("[OK] venv déjà existant")

# === 3. Installation des dépendances ===
if not os.path.isfile(requirements_file):
    print(f"[ERREUR] Fichier libs.txt introuvable : {requirements_file}", file=sys.stderr)
    sys.exit(2)

try:
    subprocess.check_call([pip_bin, "install", "-r", requirements_file])
    print("[OK] Dépendances installées depuis libs.txt")
except subprocess.CalledProcessError:
    print("[ERREUR] Échec installation des dépendances", file=sys.stderr)
    sys.exit(3)

# === 4. Modification de preferences.xml ===
if not os.path.exists(config_path):
    print(f"[ERREUR] Fichier preferences.xml introuvable : {config_path}", file=sys.stderr)
    sys.exit(4)

try:
    tree = ET.parse(config_path)
    root = tree.getroot()
except ET.ParseError as e:
    print(f"[ERREUR] Fichier XML invalide : {e}", file=sys.stderr)
    sys.exit(5)

found = False
for group in root.iter("group"):
    if group.attrib.get("id") == "extensions":
        group.set("python-interpreter", python_bin)
        found = True
        break

if not found:
    print("[ERREUR] Balise <group id=\"extensions\"> introuvable dans le fichier XML", file=sys.stderr)
    sys.exit(6)

tree.write(config_path, encoding="utf-8", xml_declaration=True)
print(f"[OK] Chemin Python injecté dans preferences.xml : {python_bin}")

# === 5. Déploiement des fichiers dans extensions/ ===
files_to_copy = [
    "bezierIntersect.inx", "colorTest.inx", "laserModeEngraving.inx", "polygonIntersect.inx", "resize.py", "strokeSize.py",
    "bezierIntersect.py", "colorTest.py", "laserModeEngraving.py", "polygonIntersect.py", "save.inx", "vectorText.inx",
    "closedShape.inx", "laserModeCutout.inx", "laserModeScanning.inx", "save.py", "vectorText.py",
    "closedShape.py", "laserModeCutout.py", "laserModeScanning.py", "resize.inx", "StrokeSize.inx", "testBatteries.py",
    "testBatteries.inx", "isolatedElement.py", "isolatedElement.inx", "tooSmallObject.py","tooSmallObject.inx", "drawArrow.py"
]

os.makedirs(extensions_dir, exist_ok=True)
source_dir = os.path.dirname(__file__)

for filename in files_to_copy:
    src_path = os.path.join(source_dir, filename)
    dst_path = os.path.join(extensions_dir, filename)
    if not os.path.isfile(src_path):
        print(f"[AVERTISSEMENT] Fichier manquant, ignoré : {filename}", file=sys.stderr)
        continue
    shutil.copy2(src_path, dst_path)
    print(f"[OK] Copié : {filename} → {extensions_dir}")
