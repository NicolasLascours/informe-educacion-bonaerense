# Expansión y matrícula del sistema educativo bonaerense

Análisis de la estructura del sistema educativo de la Provincia de Buenos Aires, la evolución de la matrícula entre 2015 y 2025, la expansión de la oferta entre 2020 y 2026 y el abandono en el nivel secundario entre 2010-11 y 2023-24. Usa datos abiertos de la Dirección General de Cultura y Educación y de la Dirección Provincial de Estadística de la Provincia de Buenos Aires.

**Informe**: https://NicolasLascours.github.io/informe-educacion-bonaerense/

## Estructura

- `notebooks/`: los análisis (01 establecimientos, 02 matrícula 2015–2025, 03 expansión, 04 abandono) y el informe de síntesis (05).
- `src/`: funciones compartidas (`utils.py`) y el script que genera el informe (`publicar_informe.py`).
- `data/raw/`: los datos de entrada, sin modificar.
- `outputs/`: gráficos y tablas que generan los notebooks.
- `docs/`: el informe publicado en GitHub Pages (`index.html`).

## Cómo reproducir

1. Instalar las dependencias: `pip install -r requirements.txt` (Python 3.14).
2. Ejecutar los notebooks 01 a 04 en orden (`jupyter nbconvert --to notebook --execute --inplace notebooks/0X_....ipynb`).
3. Generar el informe: `python src/publicar_informe.py` (ejecuta el 05 y crea `docs/index.html`).

Las decisiones, supuestos e inconsistencias de los datos están en [DOCUMENTACION.md](DOCUMENTACION.md).

## Autor

Nicolás Lascours · [LinkedIn](https://www.linkedin.com/in/nicolas-lascours/)
