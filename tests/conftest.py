import os
import sys

# Determina la ruta del directorio raíz del proyecto
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Añadir el directorio raíz del proyecto al path
sys.path.append(os.path.join(project_root, "app"))
