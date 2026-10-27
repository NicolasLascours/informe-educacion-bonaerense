"""Helpers compartidos por los notebooks del proyecto educación PBA.

Carga con tipos correctos, normalización de nombres de municipio,
chequeos de calidad de datos, guardado de figuras/tablas y control de
cifras citadas en los markdown.
"""

from __future__ import annotations

import hashlib
import json
import numbers
import re
import unicodedata
from pathlib import Path

import pandas as pd

# ---------------------------------------------------------------------------
# Rutas
# ---------------------------------------------------------------------------
PROJECT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_DIR / "data" / "raw"
OUTPUTS_DIR = PROJECT_DIR / "outputs"
NOTEBOOKS_DIR = PROJECT_DIR / "notebooks"

ARCHIVO_ESTABLECIMIENTOS = "establecimientos-educativos-19102026.csv"
# Descarga anterior, truncada en la fila 490. Se conserva solo como referencia.
ARCHIVO_ESTABLECIMIENTOS_TRUNCADO = "establecimientos_educativos.csv"
ARCHIVO_MATRICULA_MUNICIPIOS = "evolucion-unidades-servicio-y-matricula-municipios-2015_2025.xlsx"
ARCHIVO_MATRICULA_REGIONES = "evolucion-unidades-servicio-y-matricula-region-educativa-2015_2025.xlsx"
ARCHIVO_EXPANSION = "expansion-sistema-educativo-21092026.csv"
ARCHIVO_ABANDONO = "11_tasa_de_abandono_del_nivel_secundario.xlsx"

FUENTE_ESTABLECIMIENTOS = (
    "Fuente: DGCyE PBA, Establecimientos educativos (catalogo.datos.gba.gob.ar), periodo Inicial 2026"
)
FUENTE_MATRICULA = (
    "Fuente: DGCyE PBA, Unidades de servicio y matrícula 2015–2025 (catalogo.datos.gba.gob.ar)"
)
FUENTE_ABANDONO = (
    "Fuente: Dirección Provincial de Estadística PBA, Tasa de abandono del nivel secundario por municipio "
    "(datos.estadistica.ec.gba.gov.ar)"
)
FUENTE_EXPANSION = (
    "Fuente: DGCyE PBA, Expansión del sistema educativo 2020–2026 (catalogo.datos.gba.gob.ar)"
)

# ---------------------------------------------------------------------------
# Normalización de municipios
# ---------------------------------------------------------------------------
# Variante -> nombre canónico. El canónico es el que usan los archivos que
# traen municipio_id (establecimientos y expansión). Para agregar un caso,
# sumar una entrada acá; no hace falta tocar nada más.
MUNICIPIOS_NORMALIZADOS: dict[str, str] = {
    # Detectadas en el archivo de matrícula por municipio 2015–2025
    "Veinticinco de Mayo": "25 de Mayo",
    "Nueve de Julio": "9 de Julio",
    "Gonzáles Chaves": "Adolfo Gonzales Chaves",
    "Puan": "Puán",
    "Juárez": "Benito Juárez",
    "Ituzaingo": "Ituzaingó",
    "Coronel Rosales": "Coronel de Marina Leonardo Rosales",
    "General Madariaga": "General Juan Madariaga",
    # Variantes conocidas en otras fuentes, no vistas aún en estos archivos
    "Gonzales Chaves": "Adolfo Gonzales Chaves",
    "General Gonzales Chaves": "Adolfo Gonzales Chaves",
    "Juarez": "Benito Juárez",
}


def clave_texto(texto) -> str:
    """Minúsculas, sin tildes y sin espacios repetidos (para comparar nombres)."""
    if pd.isna(texto):
        return ""
    sin_tildes = "".join(
        c for c in unicodedata.normalize("NFKD", str(texto)) if not unicodedata.combining(c)
    )
    return re.sub(r"\s+", " ", sin_tildes).strip().lower()


def normalizar_municipio(serie: pd.Series) -> pd.Series:
    """Aplica MUNICIPIOS_NORMALIZADOS a una serie de nombres de municipio."""
    limpia = serie.astype("string").str.strip().str.replace(r"\s+", " ", regex=True)
    return limpia.replace(MUNICIPIOS_NORMALIZADOS)


def comparar_municipios(nombres: dict[str, pd.Series]) -> pd.DataFrame:
    """Matriz municipio x archivo (antes y después de normalizar).

    `nombres` mapea etiqueta de archivo -> serie de municipio_nombre crudo.
    Devuelve una fila por nombre crudo que no está en todos los archivos,
    con su versión normalizada y si, ya normalizado, aparece en cada archivo.
    """
    crudos = {k: set(v.dropna().unique()) for k, v in nombres.items()}
    normalizados = {
        k: set(normalizar_municipio(pd.Series(sorted(v)))) for k, v in crudos.items()
    }
    todos = set().union(*crudos.values())
    en_todos = set.intersection(*crudos.values())
    filas = []
    for nombre in sorted(todos - en_todos):
        canon = MUNICIPIOS_NORMALIZADOS.get(nombre, nombre)
        fila = {"nombre_crudo": nombre, "nombre_normalizado": canon}
        for k in nombres:
            fila[f"crudo_en_{k}"] = nombre in crudos[k]
            fila[f"normalizado_en_{k}"] = canon in normalizados[k]
        filas.append(fila)
    return pd.DataFrame(filas)


# ---------------------------------------------------------------------------
# Carga
# ---------------------------------------------------------------------------
# Identificadores: siempre string para no perder ceros a la izquierda.
COLUMNAS_ID = ["municipio_id", "cueanexo", "cui", "clave", "cue"]


def cargar_establecimientos(archivo: str = ARCHIVO_ESTABLECIMIENTOS) -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / archivo, dtype={c: "string" for c in COLUMNAS_ID})
    for col in ["matricula", "varones", "mujeres", "secciones", "establecimiento_id",
                "anexo", "nro_escuela", "desfavorabilidad"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")
    for col in ["latitud", "longitud"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def cargar_expansion(archivo: str = ARCHIVO_EXPANSION) -> pd.DataFrame:
    df = pd.read_csv(DATA_DIR / archivo, dtype={c: "string" for c in COLUMNAS_ID})
    df["fecha_acto"] = pd.to_datetime(df["fecha_acto"], format="%d/%m/%Y", errors="coerce")
    for col in ["latitud", "longitud"]:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    return df


def cargar_matricula_municipios(archivo: str = ARCHIVO_MATRICULA_MUNICIPIOS) -> pd.DataFrame:
    df = pd.read_excel(DATA_DIR / archivo)
    df["municipio_nombre_original"] = df["municipio_nombre"]
    df["municipio_nombre"] = normalizar_municipio(df["municipio_nombre"])
    return df


def cargar_matricula_regiones(archivo: str = ARCHIVO_MATRICULA_REGIONES) -> pd.DataFrame:
    return pd.read_excel(DATA_DIR / archivo)


CODIGO_TOTAL_PROVINCIA = "000"


def cargar_abandono(archivo: str = ARCHIVO_ABANDONO) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Tasa de abandono del secundario. Devuelve (municipios, total_provincia).

    `municipio_id` = "06" + código de 3 dígitos (mismo id que el padrón y la
    expansión). `anio_inicio` es el año de la matrícula base del ciclo
    ("2015-16" -> 2015). El total provincial (código 000) va en una tabla
    aparte para que no se mezcle con los municipios.
    """
    df = pd.read_excel(DATA_DIR / archivo, dtype={"COD_MUNICIPIO": "string"})
    df = df.rename(columns={
        "COD_MUNICIPIO": "cod_municipio",
        "MUNICIPIO": "municipio_nombre_original",
        "PERIODO": "periodo",
        "VALOR": "abandono_pct",
    })
    df["anio_inicio"] = df["periodo"].str.slice(0, 4).astype(int)
    df["municipio_id"] = "06" + df["cod_municipio"]
    es_total = df["cod_municipio"] == CODIGO_TOTAL_PROVINCIA
    return df[~es_total].reset_index(drop=True), df[es_total].reset_index(drop=True)


def hash_datos(*archivos: str, largo: int = 7) -> str:
    """Hash corto (sha1) del contenido de los archivos de datos en DATA_DIR.

    Solo mira los datos de entrada: editar un notebook no cambia el hash.
    """
    h = hashlib.sha1()
    for archivo in archivos:
        h.update((DATA_DIR / archivo).read_bytes())
    return h.hexdigest()[:largo]


def hash_por_archivo(archivos: dict[str, str]) -> str:
    """Hash corto de cada archivo, auditable: 'exp=abc1234;padron=d62f13c'."""
    return ";".join(f"{etiqueta}={hash_datos(archivo)}" for etiqueta, archivo in archivos.items())


# Niveles que no tienen matrícula propia: atienden alumnos ya matriculados en otra escuela.
SERVICIOS_SIN_MATRICULA_PROPIA = [
    "Educación Física (C.E.F.)",
    "Psicología Comunitaria y Pedagogía Social (C.E.C)",
]


def preparar_padron_analisis(df: pd.DataFrame) -> pd.DataFrame:
    """Universo de análisis del padrón, con el mismo criterio que el notebook 01.

    Excluye periodo "Nueva" y FinEs sin secciones con matrícula; agrega
    `matricula_sistema` (0 en C.E.F. y C.E.C.) y `region_numero`.
    """
    es_nueva = df["periodo"] == "Nueva"
    es_sin_secciones = (
        (df["secciones"] == 0) & (df["matricula"] > 0) & (df["modalidad"] != "Educación Especial")
    )
    out = df[~es_nueva & ~es_sin_secciones].copy()
    es_servicio = out["nivel"].isin(SERVICIOS_SIN_MATRICULA_PROPIA)
    out["matricula_sistema"] = out["matricula"].where(~es_servicio, 0)
    out["region_numero"] = out["region_educativa"].str.extract(r"(\d+)", expand=False).astype(int)
    return out


# ---------------------------------------------------------------------------
# Chequeos de calidad (reportan, nunca corrigen)
# ---------------------------------------------------------------------------
# Bounding box aproximado de la Provincia de Buenos Aires (con margen).
BBOX_PBA = {"lat_min": -41.2, "lat_max": -33.2, "lon_min": -63.5, "lon_max": -56.6}

NULOS_ESPERABLES = {"telefono", "rpv", "email", "turnos", "resolucion"}


def resumen_nulos(df: pd.DataFrame, esperables: set[str] = NULOS_ESPERABLES) -> pd.DataFrame:
    nulos = df.isna().sum()
    resumen = pd.DataFrame({
        "nulos": nulos,
        "pct": (nulos / len(df) * 100).round(2),
        "tipo": ["esperable" if c in esperables else "problemático" for c in df.columns],
    })
    return resumen[resumen["nulos"] > 0].sort_values("nulos", ascending=False)


def chequear_clave_unica(df: pd.DataFrame, columnas: list[str]) -> pd.DataFrame:
    """Filas que repiten la clave indicada (vacío = la clave es única)."""
    return df[df.duplicated(subset=columnas, keep=False)].sort_values(columnas)


def chequear_genero(df: pd.DataFrame) -> pd.DataFrame:
    """Filas con varones + mujeres distinto de matrícula (incluye nulos)."""
    suma = df["varones"] + df["mujeres"]
    distinto = (suma != df["matricula"]).fillna(True)
    out = df.loc[distinto].copy()
    out["diferencia"] = out["matricula"] - (out["varones"] + out["mujeres"])
    return out


def chequear_coordenadas(df: pd.DataFrame, bbox: dict = BBOX_PBA) -> pd.DataFrame:
    """Filas con lat/long nulas o fuera del bounding box de PBA."""
    dentro = df["latitud"].between(bbox["lat_min"], bbox["lat_max"]) & df["longitud"].between(
        bbox["lon_min"], bbox["lon_max"]
    )
    return df.loc[~dentro]


def chequear_filas_incompletas(df: pd.DataFrame, umbral: float = 0.5) -> pd.DataFrame:
    """Filas con más de `umbral` de columnas nulas (p. ej. filas truncadas)."""
    return df[df.isna().mean(axis=1) > umbral]


def reporte_calidad_establecimientos(df: pd.DataFrame) -> dict[str, pd.DataFrame | pd.Series]:
    """Corre todos los chequeos sobre el archivo de establecimientos."""
    return {
        "nulos": resumen_nulos(df),
        "filas_incompletas": chequear_filas_incompletas(df),
        "periodo": df["periodo"].value_counts(dropna=False),
        "duplicados_id_nivel": chequear_clave_unica(df, ["establecimiento_id", "nivel"]),
        "duplicados_id_nivel_modalidad": chequear_clave_unica(
            df, ["establecimiento_id", "nivel", "modalidad"]
        ),
        "matricula_negativa": df[df["matricula"] < 0],
        "secciones_negativas": df[df["secciones"] < 0],
        "secciones_cero_por_modalidad": df.loc[df["secciones"] == 0, "modalidad"].value_counts(),
        "genero_distinto_matricula": chequear_genero(df),
        "coordenadas_fuera_pba": chequear_coordenadas(df),
        "largo_municipio_id": df["municipio_id"].str.len().value_counts(dropna=False),
    }


# ---------------------------------------------------------------------------
# Gráficos
# ---------------------------------------------------------------------------
# Orden categórico fijo (azul, naranja, aqua, amarillo, magenta, verde,
# violeta, rojo). La serie principal es siempre PALETA[0]; el destacado
# (p. ej. La Plata) es PALETA[1].
PALETA = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4", "#008300", "#6250d6", "#e34948"]
GRIS = "#8a8984"
TEXTO_SECUNDARIO = "#52514e"


def _cmap_divergente():
    from matplotlib.colors import LinearSegmentedColormap

    # Rojo = cae, gris neutro = sin cambio, azul = crece.
    return LinearSegmentedColormap.from_list("cae_crece", ["#e34948", "#f0efec", "#2a78d6"])


CMAP_DIVERGENTE = _cmap_divergente()


def _miles_ar(x, _pos=None) -> str:
    return f"{x:,.0f}".replace(",", ".")


def formato_miles():
    """Formatter de ejes con separador de miles con punto (es-AR)."""
    from matplotlib.ticker import FuncFormatter

    return FuncFormatter(_miles_ar)


def separar_etiquetas(valores, distancia: float) -> list[float]:
    """Posiciones y para etiquetas directas, separadas al menos `distancia`."""
    orden = sorted(range(len(valores)), key=lambda i: valores[i])
    ajustados = list(valores)
    for anterior, actual in zip(orden, orden[1:]):
        ajustados[actual] = max(ajustados[actual], ajustados[anterior] + distancia)
    return ajustados


def aplicar_estilo() -> None:
    """Estilo común: grilla y ejes recesivos, ciclo de colores fijo."""
    import matplotlib.pyplot as plt
    from cycler import cycler

    plt.rcParams.update({
        "axes.prop_cycle": cycler(color=PALETA),
        "axes.spines.top": False,
        "axes.spines.right": False,
        "axes.edgecolor": GRIS,
        "axes.grid": True,
        "grid.alpha": 0.25,
        "grid.linewidth": 0.8,
        "axes.titleweight": "bold",
        "axes.titlesize": 12,
        "axes.labelcolor": TEXTO_SECUNDARIO,
        "xtick.color": TEXTO_SECUNDARIO,
        "ytick.color": TEXTO_SECUNDARIO,
        "lines.linewidth": 2,
        "lines.markersize": 6,
        "figure.dpi": 100,
    })


def grafico_barras_h(serie: pd.Series, titulo: str, xlabel: str, ylabel: str, nombre: str,
                     fuente: str, color: str = PALETA[0]):
    """Barras horizontales ordenadas (mayor arriba), con valor rotulado. Guarda y devuelve fig."""
    import matplotlib.pyplot as plt

    s = serie.iloc[::-1]
    fig, ax = plt.subplots(figsize=(10, max(3.0, 0.42 * len(s) + 1.4)))
    ax.barh(s.index.astype(str), s.to_numpy(), color=color, height=0.7)
    for y, v in enumerate(s.to_numpy()):
        ax.annotate(_miles_ar(v), (v, y), xytext=(4, 0), textcoords="offset points",
                    va="center", fontsize=8, color=TEXTO_SECUNDARIO)
    ax.margins(x=0.12)
    ax.set_title(titulo)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    from matplotlib.ticker import MaxNLocator

    ax.xaxis.set_major_locator(MaxNLocator(5))
    ax.xaxis.set_major_formatter(formato_miles())
    ax.grid(axis="y", visible=False)
    guardar_figura(fig, nombre, fuente)
    return fig


# ---------------------------------------------------------------------------
# Salidas
# ---------------------------------------------------------------------------
def guardar_figura(fig, nombre: str, fuente: str, dpi: int = 150) -> Path:
    """Agrega la fuente al pie y guarda en outputs/ como PNG."""
    OUTPUTS_DIR.mkdir(exist_ok=True)
    fig.text(0.01, 0.005, fuente, ha="left", va="bottom", fontsize=8, color="#555555")
    fig.tight_layout(rect=(0, 0.03, 1, 1))
    ruta = OUTPUTS_DIR / f"{nombre}.png"
    fig.savefig(ruta, dpi=dpi, bbox_inches="tight")
    return ruta


def guardar_tabla(df: pd.DataFrame, nombre: str, index: bool = True) -> Path:
    OUTPUTS_DIR.mkdir(exist_ok=True)
    ruta = OUTPUTS_DIR / f"{nombre}.csv"
    df.to_csv(ruta, index=index, encoding="utf-8-sig")
    return ruta


def guardar_cifras_informe(cifras: list[tuple], notebook: str) -> pd.DataFrame:
    """Guarda `outputs/<notebook>_cifras_informe.csv` para el informe de síntesis (05).

    `cifras`: tuplas (cifra_id, valor, unidad, celda_origen, descripcion). Son
    valores ya calculados en el notebook; esto solo los deja en un archivo.
    """
    df = pd.DataFrame(cifras, columns=["cifra_id", "valor", "unidad", "celda_origen", "descripcion"])
    df["valor"] = df["valor"].astype(float).round(4)
    df.insert(3, "notebook", notebook)
    assert df["cifra_id"].is_unique, "cifra_id repetido"
    guardar_tabla(df, f"{notebook}_cifras_informe", index=False)
    return df


def leer_cifra(archivo: str, fila: str, columna: str, columna_indice: str | None = None) -> float:
    """Lee un valor ya guardado en outputs/ (sin calcular nada).

    `columna_indice`: columna que identifica la fila; si es None, la primera columna.
    """
    df = pd.read_csv(OUTPUTS_DIR / archivo, encoding="utf-8-sig")
    clave = columna_indice or df.columns[0]
    fila_df = df[df[clave].astype(str) == str(fila)]
    assert len(fila_df) == 1, f"{archivo}: fila {fila!r} no encontrada o repetida"
    return float(fila_df[columna].iloc[0])


def hash_outputs(archivos: list[str], largo: int = 7) -> str:
    """Hash corto del contenido de archivos de outputs/ (los CSV que lee el informe)."""
    h = hashlib.sha1()
    for archivo in archivos:
        h.update((OUTPUTS_DIR / archivo).read_bytes())
    return h.hexdigest()[:largo]


def exportar_og_image(png: Path, salida: Path, ancho: int = 1200, alto: int = 630, margen: float = 0.04) -> Path:
    """Centra un PNG existente en un lienzo de ancho×alto px (vista previa de LinkedIn).

    Es procesamiento de imagen sobre un gráfico ya generado: no recalcula datos.
    """
    import matplotlib.image as mpimg
    import matplotlib.pyplot as plt

    imagen = mpimg.imread(png)
    alto_img, ancho_img = imagen.shape[:2]
    escala = min(ancho * (1 - 2 * margen) / ancho_img, alto * (1 - 2 * margen) / alto_img)
    w, h = ancho_img * escala, alto_img * escala
    x0, y0 = (ancho - w) / 2, (alto - h) / 2

    fig = plt.figure(figsize=(ancho / 100, alto / 100), dpi=100)
    ax = fig.add_axes((0, 0, 1, 1))
    ax.axis("off")
    ax.set_xlim(0, ancho)
    ax.set_ylim(alto, 0)
    ax.imshow(imagen, extent=(x0, x0 + w, y0 + h, y0), interpolation="lanczos")
    Path(salida).parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(salida, dpi=100, facecolor="white")
    plt.close(fig)
    return Path(salida)


def insertar_meta_og(html: Path, titulo: str, descripcion: str, url_pagina: str, url_imagen: str) -> None:
    """Agrega las etiquetas Open Graph (vista previa en LinkedIn) al <head> de un HTML."""
    from html import escape

    etiquetas = "\n".join([
        f'<meta property="og:title" content="{escape(titulo)}">',
        f'<meta property="og:description" content="{escape(descripcion)}">',
        f'<meta property="og:image" content="{escape(url_imagen)}">',
        '<meta property="og:image:width" content="1200">',
        '<meta property="og:image:height" content="630">',
        f'<meta property="og:url" content="{escape(url_pagina)}">',
        '<meta property="og:type" content="article">',
        '<meta name="twitter:card" content="summary_large_image">',
    ])
    texto = Path(html).read_text(encoding="utf-8")
    assert "<head>" in texto and 'property="og:title"' not in texto
    Path(html).write_text(texto.replace("<head>", "<head>\n" + etiquetas, 1), encoding="utf-8")


def cagr(valor_inicial, valor_final, anios: int):
    """Tasa de crecimiento anual compuesta, en %."""
    return ((valor_final / valor_inicial) ** (1 / anios) - 1) * 100


# ---------------------------------------------------------------------------
# Control de cifras citadas en markdown
# ---------------------------------------------------------------------------
_PATRON_MARCA = re.compile(r"<!--\s*verificado\s+(\S+),\s*hash datos:\s*([\w=;]+),\s*id:\s*([\w-]+)\s*-->")


_PATRON_NUMERO = re.compile(r"[−+\-]?\d{1,3}(?:\.\d{3})+(?:,\d+)?|[−+\-]?\d+(?:,\d+)?")


def parsear_numero_ar(texto: str) -> tuple[float, int]:
    """Último número del fragmento, en formato es-AR, y sus decimales.

    'Región 6: −8,76 %' -> (-8.76, 2); 'pasó de 4.914.177' -> (4914177.0, 0).
    """
    encontrados = _PATRON_NUMERO.findall(texto)
    if not encontrados:
        raise ValueError(f"No hay número en {texto!r}")
    t = encontrados[-1].replace("−", "-").replace("+", "")
    t = t.replace(".", "").replace(",", ".")
    decimales = len(t.split(".")[1]) if "." in t else 0
    return float(t), decimales


def _archivos_cambiados(hash_marca: str, hash_actual: str) -> str:
    """Con hashes por archivo ('exp=...;padron=...'), indica cuáles cambiaron."""
    if "=" not in hash_marca or "=" not in hash_actual:
        return ""
    antes = dict(p.split("=") for p in hash_marca.split(";"))
    ahora = dict(p.split("=") for p in hash_actual.split(";"))
    cambiados = [k for k in ahora if antes.get(k) != ahora[k]]
    return f"; cambió: {', '.join(cambiados)}" if cambiados else ""


def _comparar_conjunto(fragmento: str, esperado: set) -> tuple[str, str, bool]:
    """Compara la lista de entidades citada en el fragmento con el conjunto calculado."""
    if all(isinstance(x, numbers.Integral) for x in esperado):
        tokens = re.findall(r"\d+(?:,\d+)?", fragmento)
        citados = {int(t) for t in tokens if "," not in t}
        esperado = {int(x) for x in esperado}
        return str(sorted(citados)), str(sorted(esperado)), citados == esperado
    faltan = sorted(x for x in esperado if not re.search(re.escape(str(x)) + r"(?![\w])", fragmento))
    mostrado = str(sorted(esperado)) + (f" | faltan: {faltan}" if faltan else "")
    return "lista de nombres", mostrado, not faltan


def _markdowns_marcados(ruta_notebook: Path) -> dict[str, dict]:
    nb = json.loads(Path(ruta_notebook).read_text(encoding="utf-8"))
    marcados = {}
    for i, celda in enumerate(nb["cells"]):
        if celda["cell_type"] != "markdown":
            continue
        texto = "".join(celda["source"])
        m = _PATRON_MARCA.search(texto)
        if m:
            marcados[m.group(3)] = {"celda": i, "texto": texto, "fecha": m.group(1), "hash": m.group(2)}
    return marcados


def verificar_citas(
    ruta_notebook: Path, citas: list[tuple], hash_actual: str, estricto: bool = True,
    guardar_como: str | None = None,
) -> pd.DataFrame:
    """Compara los números citados en markdown con los calculados.

    `citas`: tuplas (id_markdown, fragmento_citado, valor_calculado). El
    fragmento tiene que aparecer literal en el markdown marcado con ese id.
    Según el tipo de `valor_calculado`:
    - número: se compara con el último número del fragmento, con la
      precisión con la que está escrito;
    - conjunto de enteros (p. ej. regiones): los enteros sueltos del
      fragmento (sin decimales) tienen que ser exactamente ese conjunto;
    - conjunto de textos (p. ej. municipios): cada nombre tiene que
      aparecer en el fragmento (detecta omisiones).
    Lee el .ipynb guardado en disco. No modifica textos: con `estricto=True`
    lanza AssertionError si hay diferencias; con False solo las imprime.
    Si se indica `guardar_como`, la tabla completa se guarda en outputs/
    antes de fallar.
    """
    marcados = _markdowns_marcados(ruta_notebook)
    filas = []
    for id_md, citado, calculado in citas:
        md = marcados.get(id_md)
        if md is None:
            filas.append((id_md, None, citado, None, calculado, "MISMATCH: markdown no encontrado"))
            continue
        if isinstance(calculado, (set, frozenset)):
            valor, mostrado, coincide = _comparar_conjunto(citado, calculado)
        else:
            valor, dec = parsear_numero_ar(citado)
            mostrado = round(float(calculado), max(dec, 2))
            coincide = abs(valor - calculado) <= 0.5 * 10 ** (-dec) + 1e-9
        if citado not in md["texto"]:
            estado = "MISMATCH: texto no está en el markdown"
        elif not coincide:
            estado = "MISMATCH"
        elif md["hash"] != hash_actual:
            estado = "OK (hash de datos distinto: revisar" + _archivos_cambiados(md["hash"], hash_actual) + ")"
        else:
            estado = "OK"
        filas.append((id_md, md["celda"], citado, valor, mostrado, estado))
    tabla = pd.DataFrame(
        filas, columns=["markdown", "celda", "texto_citado", "valor_citado", "valor_calculado", "estado"]
    )
    if guardar_como:
        guardar_tabla(tabla, guardar_como, index=False)
    errores = tabla[~tabla["estado"].str.startswith("OK")]
    if not errores.empty:
        aviso = (
            "\n" + "#" * 70 + f"\n# {len(errores)} CIFRA(S) CITADA(S) NO COINCIDEN CON EL CÁLCULO\n"
            + "#" * 70 + "\n" + errores.to_string(index=False)
        )
        if estricto:
            raise AssertionError(aviso)
        print(aviso)
    return tabla
