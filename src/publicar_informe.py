"""Genera el informe de síntesis publicable: docs/index.html y docs/og-image.png.

Uso, desde la raíz del proyecto (con los notebooks 01–04 ya ejecutados):
    .venv\\Scripts\\python src\\publicar_informe.py

Pasos:
1. Ejecuta notebooks/05_informe_sintesis.ipynb y lo guarda con sus outputs
   (la celda de control falla si alguna cifra del texto no coincide con outputs/).
2. Lo exporta a HTML autocontenido, sin celdas de código y sin las celdas
   marcadas con la etiqueta "ocultar" (configuración y control).
3. Arma docs/og-image.png (1200×630) a partir de outputs/02_matricula_docentes_indice.png.
4. Inserta las etiquetas Open Graph para la vista previa en LinkedIn.
"""

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import utils as u

NOTEBOOK = u.NOTEBOOKS_DIR / "05_informe_sintesis.ipynb"
DOCS = u.PROJECT_DIR / "docs"
IMAGEN_DESTACADA = u.OUTPUTS_DIR / "02_matricula_docentes_indice.png"


def main() -> None:
    config = json.loads((u.PROJECT_DIR / "informe_config.json").read_text(encoding="utf-8"))
    pendientes = [clave for clave, valor in config.items() if "[COMPLETAR]" in str(valor)]
    if pendientes:
        print("AVISO: faltan datos en informe_config.json:", ", ".join(pendientes))
        print("       El HTML se genera igual, pero con [COMPLETAR] visible y enlaces incompletos.")

    nbconvert = [sys.executable, "-m", "nbconvert"]
    subprocess.run(nbconvert + ["--to", "notebook", "--execute", "--inplace", str(NOTEBOOK)], check=True)
    DOCS.mkdir(exist_ok=True)
    subprocess.run(nbconvert + [
        "--to", "html", "--no-input", "--embed-images",
        "--TagRemovePreprocessor.enabled=True",
        "--TagRemovePreprocessor.remove_cell_tags=ocultar",
        "--output", "index", "--output-dir", str(DOCS), str(NOTEBOOK),
    ], check=True)

    u.exportar_og_image(IMAGEN_DESTACADA, DOCS / "og-image.png")

    url_pagina = config.get("url_github_pages") or f"https://{config['usuario_github']}.github.io/{config['repo']}/"
    u.insertar_meta_og(DOCS / "index.html", config["og_titulo"], config["og_descripcion"],
                       url_pagina, url_pagina + "og-image.png")
    print("Listo:", DOCS / "index.html", "y", DOCS / "og-image.png")
    print("URL prevista en GitHub Pages:", url_pagina)


if __name__ == "__main__":
    main()
