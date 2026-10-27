# Documentación de cambios y decisiones

> **Estado (2026-10-27): proyecto terminado.** Los notebooks 01 a 05 corren de punta a punta sin errores con `MODO_ESTRICTO = True`. Control de cifras: 01 32/32, 02 190/190 (eran 183 antes de agregar los hallazgos de docentes y jardines), 03 82/82, 04 78/78 y 05 101/101 OK. El informe publicable está en `docs/index.html` (con `docs/og-image.png`). `informe_config.json` está completo (autor, usuario de GitHub y LinkedIn), así que la portada, el footer y las etiquetas de LinkedIn ya salen con esos datos.

## 1. Resumen ejecutivo

### Notebook 01 — Establecimientos
- **Archivo nuevo**: usa el CSV completo descargado el 2026-10-21 (`establecimientos-educativos-19102026.csv`: 21.593 filas, 135 municipios, 25 regiones). El archivo anterior estaba truncado en la fila 490 (§3) y se conserva sin tocar, solo como referencia.
- **Alcance**: Parte A, panorama de los municipios presentes en el padrón (hoy los 135): totales, distribuciones, top 10 de establecimientos (total y Nivel Secundario), rankings de municipios y regiones, y mapa. Parte B, La Plata como caso de estudio, con estatal y privado juntos.
- **Calidad de datos al inicio**: tipos, nulos, rangos, coordenadas, periodo, la clave única `establecimiento_id + nivel + modalidad` (§2.2), nombres de municipio y comparación con el archivo truncado.
- **Fuera del análisis, reportadas en la sección 4**: 115 ofertas "Nueva" y 3 filas de FinEs sin secciones.
- **Matrícula del sistema** (tercera ronda): los C.E.F. y C.E.C. siguen en el análisis de oferta, pero sus alumnos atendidos (186.874) no se suman. Todas las sumas, rankings, el top 10 y La Plata usan `matricula_sistema`. La sección 4 incluye la verificación (CUI y municipio), el top 10 de servicios y la auditoría del total.
- **Textos de La Plata corregidos** (segunda ronda): "sistema educativo estatal y privado", y el duplicado del 10474 explicado en el resumen. Se aclara también que las escuelas agrarias están incluidas en el top 10 de Secundario.
- Control de cifras citadas: 32/32 OK.

### Notebook 02 — Matrícula 2015–2025
- **Nueva sección 1 de calidad de datos**: tipos, nulos, unicidad de las claves, normalización de los 8 nombres de municipio y validación de la suma de municipios contra la suma de regiones (unidades y matrícula coinciden exactamente; docentes ±2,6 por redondeo).
- **Agregados**: variación % y CAGR 2015→2025 (total, por región y por municipio); top 10 que más crecen, que más caen y por matrícula 2025; 5 gráficos nuevos (total PBA por año, variación por región, top 5 regiones, extremos municipales y heatmap municipio × año). Los 7 gráficos existentes ahora tienen fuente y se guardan.
- **Textos**: se mantiene tu redacción. Se corrige el 42/92 invertido de La Plata y se sacan los restos de chat y tutorial. Cada markdown con cifras lleva `<!-- verificado …, hash datos: …, id: … -->`.
- **Celda de control**: en la primera ronda dio 167/168 OK y detectó el error de las unidades por región (§5.6). Ese texto ya está corregido. Además, el control ahora verifica **listas de entidades** ("las Regiones 1, 3, 5, 10, 11, 17 y 18"), no solo valores. Resultado actual: **183/183 OK**.
- Nota en el heatmap: el pico de Mar Chiquita en 2023 viene del relevamiento, no del análisis.

### Notebook 03 — Expansión 2020–2026 (nuevo)
- **Unidad de análisis: el evento** (519 actos en 115 municipios), no el establecimiento. Donde un cruce necesita establecimientos únicos (518), se aclara y no se mezclan unidades.
- **Calidad de datos**: mismo estándar que 01 y 02. Incluye el establecimiento con dos eventos (102873), la verificación de nombres de municipio y la asignación de región desde el padrón, con dos `assert`: cada municipio tiene una sola región, y la región por municipio coincide con la región por `cueanexo`.
- **Contenido**:
  - Eventos por año y tipo, con el pico 2022–2023 desagregado.
  - Tipo de organización, ámbito (comparado con el padrón) y documento.
  - Territorio con eventos absolutos y dos tasas, con IC aproximado y marca de base.
  - Cruce con el padrón: 517 de 519 con par, 2 CIIE sin par con su hipótesis, 24 ofertas "Nueva".
  - Cruce con la serie 2015–2025 (ventana principal 2020→2025), San Vicente y casos candidatos para el 05.
- **Control de cifras**: 82/82 OK, incluidas 6 listas. La marca de verificación lleva el hash de cada uno de los tres archivos que lee.

### Notebook 04 — Abandono en el nivel secundario 2010-11 a 2023-24 (nuevo)
- **Fuente**: `11_tasa_de_abandono_del_nivel_secundario.xlsx` (Dirección Provincial de Estadística). Son 14 ciclos y 135 municipios, más el total provincial, que va en una tabla aparte (`utils.cargar_abandono`).
- **Calidad de datos**:
  - Cruce por código: "06" + código = `municipio_id`.
  - Una variante de nombre nueva (Rosales), que no se agrega al diccionario.
  - 1 nulo (Lezama 2010-11), 124 negativos marcados y no corregidos, 0 valores mayores a 100 y el cambio de precisión en 2023-24.
  - Hay `assert` para que el total provincial no se cuele en municipios ni regiones.
- **Contenido**:
  - Serie provincial, con 2020-21 marcado y tramos con y sin él.
  - Municipios: mediana 2021-22 a 2023-24 como principal, promedio como secundario y mediana con 2020-21 como sensibilidad. Cambio robusto y entre extremos, y heatmap divergente centrado en 0.
  - Regiones: mediana como principal y ponderado por la matrícula secundaria 2026 como sensibilidad, lado a lado.
  - Cruces con el 02, el 03 y el 01, y casos candidatos para el 05.
- **Control de cifras**: 78/78 OK, incluidas 12 listas. La marca lleva el hash de los 4 archivos que lee.

### Notebook 05 — Informe de síntesis (nuevo)
- **No es un notebook de análisis**: no calcula nada. Muestra gráficos ya generados en `outputs/` y tablas leídas de los CSV de `outputs/`, y arma el texto.
- **Estructura**:
  - Portada: título, subtítulo, autor, fecha, repositorio, enlaces a los cuatro datasets e imagen destacada.
  - Resumen ejecutivo: 6 viñetas con "qué significa" y un párrafo de síntesis.
  - Seis hallazgos: estructura, matrícula, divergencia municipal, expansión, abandono y asociaciones.
  - Conclusión: qué muestran los datos, qué no y próximos pasos.
  - Cómo reproducir y footer con el enlace a esta documentación.
- **Control de cifras**: 77/77 OK. Cada cifra del texto se compara con una celda concreta de un CSV de `outputs/` (`utils.leer_cifra`), incluida la descripción para LinkedIn.
- **Salida**: `docs/index.html` (HTML autocontenido, sin código y sin la sección de control) y `docs/og-image.png` (1200×630), generados con `src/publicar_informe.py`.

### Estado final
- **01**: Restart & Run All sin errores ni warnings. Totales finales del informe:

  | Total | Valor |
  |---|---|
  | **Matrícula total del sistema** (sin C.E.F., C.E.C., "Nueva" ni FinEs sin secciones) | **4.690.724** |
  | Ofertas (filas establecimiento × nivel × modalidad) | 21.475 |
  | Establecimientos únicos | 19.738 |
  | Secciones | 208.915 |
  | Alumnos atendidos en C.E.F. y C.E.C. (se reportan, no se suman) | 186.874 |
  | Municipios / regiones | 135 / 25 |

  Las ofertas, establecimientos y secciones incluyen a los C.E.F. y C.E.C., porque son oferta real. La auditoría del total está en §3 y en `outputs/01_auditoria_matricula_total.csv`.
- **02**: Restart & Run All sin errores con `MODO_ESTRICTO = True`.
- **03**: Restart & Run All sin errores con `MODO_ESTRICTO = True`. Totales:

  | Total | Valor |
  |---|---|
  | Eventos de expansión (23/04/2020 – 02/09/2026) | 519 (518 establecimientos únicos, 115 municipios) |
  | Con par en el padrón por `cueanexo` | 517 (493 con matrícula y 24 en ofertas "Nueva") |
  | Sin par | 2, los dos CIIE (Lezama 2022 y Alberti 2025) |
  | Ofertas "Nueva" del año 2023, todavía sin matrícula | 3 |
  | Pico 2022–2023 | 286 eventos (55,1 %) |
  | Eventos rurales / establecimientos rurales del padrón | 27,6 % / 15,4 % |
  | Spearman entre eventos cada 10.000 alumnos y variación de matrícula 2020→2025 | 0,36 (115 municipios con eventos); 0,25 con los 135 |

- **04**: Restart & Run All sin errores con `MODO_ESTRICTO = True`. Totales:

  | Total | Valor |
  |---|---|
  | Municipios / ciclos | 135 / 14 (2010-11 a 2023-24) |
  | Valores con dato | 1.889 (1 nulo: Lezama 2010-11) |
  | Negativos | 124 (6,6 % de los valores con dato); 39 en 2020-21 y 21 en 2019-20 |
  | Total provincial | 8,9 % (2010-11) → 2,84 % (2023-24); 2020-21 atípico: 0,4 % |
  | Municipios que bajan el abandono (mediana 2015-18 → 2021-24) | 112 de 135 (mediana del cambio −2,1 pp) |
  | Correlaciones con matrícula (02), expansión secundaria (03) y estructura del padrón (01) | todas por debajo de 0,1 en valor absoluto |

- **Outputs** (`outputs/`): 37 PNG (12 del 01, 12 del 02, 7 del 03 y 6 del 04) y 55 CSV (20 del 01, 9 del 02, 14 del 03 y 12 del 04), incluidas las tablas de control `0X_control_citas.csv`.

## 2. Decisiones tomadas y por qué

### 2.1 Identificadores como string
- **Decisión**: `municipio_id`, `cueanexo`, `cui`, `clave` y `cue` se leen como string (`utils.COLUMNAS_ID`).
- **Motivo**: en los CSV originales `municipio_id` viene con 5 dígitos (`06441`). Leído como int queda `6441`, y un cruce con una fuente que lo traiga como texto falla en silencio. `clave` es alfanumérica (`0001AD0003`). `cueanexo` y `cui` son códigos, no cantidades.
- **Alternativas consideradas**: leer como int y aplicar `zfill(5)` al cruzar. Se descartó porque obliga a recordarlo en cada uso.
- **Impacto**: no cambia ningún número. Evita cruces vacíos.

### 2.2 Clave única de establecimientos: `establecimiento_id + nivel + modalidad`
- **Decisión**: cada fila del CSV es una oferta establecimiento × nivel × modalidad.
- **Motivo**: `establecimiento_id + nivel` **no es única**. En la v2 hay 112 filas (56 pares) que la repiten. Ejemplo: el establecimiento **381 de Alberti** tiene dos filas de "Nivel Secundario", una de Educación Común (363 alumnos) y otra de Técnico Profesional (12). En La Plata pasa lo mismo con el 10474 (privado). Con `+ modalidad` hay 0 duplicados, y el notebook 01 lo verifica con un `assert`.
- **Regla de uso**: la **matrícula se suma** sobre filas (cada fila es una oferta distinta, así que no se duplica). Los **establecimientos se cuentan** con `establecimiento_id.nunique()`, nunca con `len()` ni sumando conteos por nivel o por categoría.
- **Alternativas consideradas**: deduplicar por `id + nivel` quedándose con la fila de mayor matrícula. Se descartó porque se pierde matrícula real (los 12 alumnos del 381).
- **Impacto**: con la clave vieja, un `drop_duplicates` habría eliminado 56 filas y su matrícula.

### 2.3 Normalización de `municipio_nombre`
- **Decisión**: diccionario `utils.MUNICIPIOS_NORMALIZADOS` (variante → canónico). El canónico es el nombre que usan los archivos que traen `municipio_id` (padrón de establecimientos y expansión), que coinciden entre sí al 100 %. Se aplica al archivo de matrícula por municipio 2015–2025, que no trae `municipio_id`. El original se conserva en `municipio_nombre_original`.
- **Las 8 equivalencias aplicadas**:

  | Variante (serie municipal 2015–2025) | Canónico | Motivo |
  |---|---|---|
  | Veinticinco de Mayo | 25 de Mayo | número escrito en letras |
  | Nueve de Julio | 9 de Julio | número escrito en letras |
  | Gonzáles Chaves | Adolfo Gonzales Chaves | nombre abreviado y tilde incorrecta |
  | Puan | Puán | falta la tilde |
  | Juárez | Benito Juárez | nombre abreviado |
  | Ituzaingo | Ituzaingó | falta la tilde |
  | Coronel Rosales | Coronel de Marina Leonardo Rosales | nombre abreviado |
  | General Madariaga | General Juan Madariaga | nombre abreviado |

  Las 4 primeras se detectaron al comparar con expansión y las otras 4 al comparar con el padrón v2. El diccionario incluye además tres variantes preventivas que no aparecen en estos archivos: "Gonzales Chaves", "General Gonzales Chaves" y "Juarez".
- **Alternativas consideradas**: (a) cruzar comparando sin tildes ni mayúsculas. No resuelve "Juárez"/"Benito Juárez" ni "Nueve"/"9", y puede dar falsos positivos. (b) Cruzar por `municipio_id`. Es lo ideal, pero la serie municipal no lo trae.
- **Impacto**: sin normalizar, 8 de los 135 municipios quedan sin cruzar.

### 2.4 Filas que no cruzan en los joins
- **Decisión**: los cruces se reportan, no se descartan en silencio. Cada notebook imprime "sin par: ninguno" o la lista de nombres sin par.
- **Resultado**: padrón y serie 2015–2025 cruzan los 135 municipios después de normalizar. Expansión tiene eventos en 115 municipios; los 20 restantes no tienen eventos, lo que no es un error. Las 489 filas válidas del archivo truncado aparecen todas en la v2, con la misma matrícula.
- **Alternativa considerada**: inner join silencioso. Se descartó porque ocultaría cualquier municipio nuevo o renombrado en una descarga futura.

### 2.5 Tratamiento de nulos
- CSV v2: solo hay nulos en columnas de contacto: `rpv` (71,8 %), `email` (2,0 %) y `turnos` (0,8 %). Se dejan y no se usan.
- Expansión: `resolucion` tiene 10 nulos (1,9 %). Se dejan.
- Serie 2015–2025: sin nulos.
- **No se imputó nada.** Los nulos "problemáticos" del archivo viejo (matrícula, nivel, etc.) eran todos de la fila truncada.

### 2.6 `secciones = 0`: no se filtra
- **Decisión**: las filas de Educación Especial con secciones = 0 se conservan en el análisis.
- **Motivo**: son 1.722 de las 1.834 filas con secciones = 0. En Educación Especial la atención no se organiza en secciones convencionales, así que es esperable.
- **Alternativa considerada**: filtrar `secciones > 0`. Solo tendría sentido para un indicador "alumnos por sección", y en ese caso se excluirían *solo para ese cálculo*, aclarándolo.
- **Impacto**: filtrarlas sacaría del análisis una parte importante de la matrícula de Educación Especial.
- Las otras 112 filas con secciones = 0 son 109 ofertas "Nueva" y 3 de FinEs; ver §2.7.

### 2.7 Filas fuera del análisis: periodo "Nueva" y FinEs sin secciones
- **Decisión (acordada)**: el análisis usa solo `periodo == "Inicial 2026"` y excluye además 3 filas de Plan FinEs con secciones = 0 y matrícula > 0. Ambos grupos se reportan en la sección 4 del 01: cantidad, distribución por nivel y modalidad, y top 10 municipios.
- **Motivo**: las 115 "Nueva" son ofertas recién creadas, con matrícula 0 y secciones 0, y ninguno de esos establecimientos aparece también con periodo "Inicial 2026". No aportan a ninguna distribución y bajarían los promedios de matrícula por establecimiento. Las 3 de FinEs tienen matrícula real (1.101 alumnos en total) pero no tienen secciones asignadas.
- **Alternativa considerada**: incluirlas como "oferta vigente" en el conteo de establecimientos.
- **Impacto**: excluir las "Nueva" resta 115 ofertas y 0 alumnos. Excluir las de FinEs resta **1.101 alumnos** y 3 ofertas de la matrícula total. Ver §5.3 y §5.4.
- **C.E.F. y C.E.C.** (tercera ronda) tienen un tratamiento distinto: **siguen** en los conteos de oferta, pero sus alumnos atendidos no se suman a la matrícula del sistema (§5.1 y §5.2).

### 2.8 Filtros aplicados
- **Sector**: no se filtra. La v2 trae 15.484 filas del sector Estatal y 6.109 del Privado. El archivo viejo parecía "solo estatal" porque estaba truncado.
- **Periodo y FinEs**: §2.7.

### 2.9 La Plata (Parte B del 01): estatal y privado juntos — *decisión con impacto en números del informe*
- **Decisión (acordada)**: el recorte de La Plata incluye los dos sectores.
- **Motivo**: la v2 es la foto completa del sistema; mostrar solo estatal sería contar la mitad. La apertura por sector queda visible al inicio de la Parte B, con la matrícula del sistema (sin el C.E.F. Nº 2 de La Plata, que es estatal): Estatal 509 establecimientos y 162.936 alumnos (59,9 % y 68,5 %); Privado 341 establecimientos y 74.867 alumnos (40,1 % y 31,5 %).
- **Cifras que cambian respecto del análisis original**:

  | Cifra | Original (archivo truncado) | Actual (v2, estatal + privado) |
  |---|---|---|
  | Filas de La Plata | 337 | 927 |
  | Establecimientos únicos | 290 | 850 |
  | Suma de establecimientos por nivel | 337 | 926 |
  | Matrícula total | 105.929 | 241.291 (237.803 sin el C.E.F., §5.1) |
  | Media / mediana de matrícula por fila | 314 / 175 | 260 / 160 |
  | Filas del archivo | 490 | 21.593 |
  | Duplicados de `id + nivel` en La Plata | 0 | 1 (el 10474) |

- **Ojo**: aun contando solo el sector estatal, el archivo viejo tenía **290 de los 509** establecimientos estatales de La Plata (105.929 de 166.424 alumnos). El corte afectaba también a La Plata, así que las cifras originales estaban incompletas más allá de la decisión de sumar los privados.
- **Textos**: se actualizaron los números de tus markdown (celdas `md-lp-niveles`, `md-lp-media` y `md-lp-resumen`, verificadas por el control). En la segunda ronda, con tu OK, se corrigieron los dos textos que no cerraban (§5.7, [RESUELTO]).

### 2.10 Top 10 por matrícula de Nivel Secundario
- **Decisión**: Nivel Secundario = modalidades **Educación Común + Educación Técnico Profesional**.
- **Motivo**: pediste "Común + Técnico Profesional + Agraria", pero en este padrón **no existe una modalidad "Agraria"**. Las Escuelas de Educación Secundaria Agraria (EESA) figuran como Técnico Profesional (107 filas) o Común (3 filas), así que ya están incluidas.
- **Qué queda fuera**: el secundario de Jóvenes y Adultos (CENS, 89.211 alumnos) y el de Educación Artística (4.384). Ver §5.5.
- **Alternativa considerada**: todo "Nivel Secundario" sin filtrar por modalidad. Mezclaría trayectorias de adultos con la escolaridad secundaria regular.

### 2.11 Control de cifras citadas en los markdown (01 y 02)
- **Decisión**: la última celda de cada notebook lee el `.ipynb` guardado en disco, busca cada cifra citada (como fragmento literal, por ejemplo "Región 6: −8,76 %") dentro del markdown marcado con su `id` y compara el último número del fragmento con el cálculo, con la precisión con la que está escrito. Si no coinciden, lanza `AssertionError`. Con `MODO_ESTRICTO = False` (celda de configuración) solo reporta. **Nunca reescribe textos.** La tabla se guarda en `outputs/0X_control_citas.csv`, también cuando falla.
- **Motivo**: el 02 tiene más de 160 cifras escritas a mano. Si cambia el dato o alguien edita un número, el texto deja de cerrar sin que nadie lo note. El control ya encontró un caso (§5.6).
- **Alternativas consideradas**: (a) generar los textos con f-strings; se descartó porque pediste mantener tu redacción. (b) Verificar solo números sueltos; un "42" aparece en varios lugares y el chequeo no probaría nada.
- **Listas de entidades** (agregado en la segunda ronda): si el valor calculado es un conjunto, se compara la lista citada. Con números (regiones, ids) se toman los enteros sueltos del fragmento, ignorando los decimales como "−7,49", y tienen que ser **exactamente** el conjunto calculado: detecta faltantes y sobrantes. Con nombres (municipios) se verifica que **ninguno falte**. Es el tipo de error que se había escapado ("las regiones 1, 3, 5, 11 y 17" sin la 10 ni la 18). Probado contra el texto viejo: lo marca como MISMATCH. Hoy verifica 9 listas: 5 de regiones, 3 de municipios y 1 de establecimientos.
- **Limitaciones**: las cifras escritas en letras ("Cinco regiones") no se verifican; conviene escribirlas con números. En listas de nombres no se detectan nombres de más. Si editás un markdown en Jupyter, guardá el notebook antes de correr el control, porque lee el archivo en disco.
- **Marca de verificación**: `<!-- verificado 2026-10-21, hash datos: XXXXXXX, id: md-… -->`. El hash es un sha1 corto **del contenido de los archivos de datos de entrada** (`utils.hash_datos`), nunca del notebook: corregir un texto no lo cambia. Valores actuales: 02 = `83dedf7` (los dos xlsx), 01 = `d62f13c` (CSV v2). Si cambian los datos, el control marca "OK (hash de datos distinto: revisar)".

### 2.12 CAGR y heatmap (02)
- **CAGR** = (valor 2025 / valor 2015)^(1/10) − 1, con 10 intervalos anuales. Es la tasa anual equivalente; no describe la trayectoria intermedia (por ejemplo, el pico de 2019).
- **Heatmap**: índice de matrícula con base 2015 = 100, no valores absolutos, porque en absolutos La Matanza y La Plata saturarían la escala. Usa una escala divergente centrada en 100.
- **Alternativa considerada**: heatmap de la variación interanual. Se descartó porque resalta el ruido de un año y oculta la trayectoria acumulada.

### 2.13 Gráficos
- Todos se guardan con `utils.guardar_figura` en `outputs/`, como PNG a 150 dpi, con título, ejes rotulados y la fuente al pie.
- Paleta fija (`utils.PALETA`): azul como serie principal, naranja como destacado (La Plata), rojo/azul para caídas/subas.
- Variables de escala distinta (matrícula, unidades, cargos) van en paneles separados o como índice base 100. Nunca se usa doble eje Y.
- El mapa del 01 es un scatter de lat/long con matplotlib. No se usó geopandas porque no hacía falta.

### 2.14 Notebook 03: unidad de análisis = evento
- **Decisión** (acordada): la unidad es el evento, con 519 casos. Un establecimiento con dos actos son dos hechos de expansión.
- **Motivo**: la expansión se mide en actos (creaciones, reaperturas, estatizaciones, anexos). Contar establecimientos únicos (518) borraría que al 102873 le pasaron dos cosas.
- **Alternativa considerada**: establecimientos únicos. Se usa **solo** en la tabla de matrícula 2026 por año del acto, donde el 102873 se cuenta una vez, en el año de su primer acto, para no sumar dos veces su matrícula. Esa tabla lo aclara en su markdown.
- **Impacto**: San Vicente tiene 19 eventos y 18 establecimientos; en el resto de los municipios eventos y establecimientos coinciden.

### 2.15 Notebook 03: región tomada del padrón
- **Decisión**: el archivo de expansión no trae región; se asigna por municipio desde el padrón.
- **Verificación previa**: los 115 municipios están en el padrón y cada uno tiene una sola región. En los 517 eventos con par, la región por `cueanexo` coincide con la región por municipio. El notebook lo controla con dos `assert`.
- **Alternativa considerada**: asignar por `cueanexo`. Se descartó porque deja sin región a los 2 eventos sin par.

### 2.16 Notebook 03: tasas territoriales, base y estabilidad
- **Decisión** (acordada):
  - Absolutos y tasas lado a lado. La tasa principal es eventos cada 10.000 alumnos de matrícula del sistema (la del 01, sin C.E.F. ni C.E.C.); la secundaria, eventos cada 100 establecimientos.
  - **No se excluye ningún municipio**: se marcan con una columna `base` (chica < 3 eventos, media 3 a 9, grande ≥ 10).
  - Se agrega un IC 95 % aproximado de Poisson (±1,96·√n). En el gráfico, los de base chica van en gris, con una nota al pie.
- **Motivo**: excluir obliga a fijar un umbral que queda como decisión no auditable; mostrar y marcar deja que el lector juzgue.
- **Efecto de la base**: las dos tasas dan rankings casi iguales (Spearman 0,90, 8 de 10 en común en los dos top 10). Lo que cambia mucho es pasar de absolutos (encabeza el conurbano) a tasas (encabezan municipios chicos). Los umbrales de `base` son de presentación, no un filtro.

### 2.17 Notebook 03: cruce con el 02
- **Decisión** (acordada): la ventana principal es 2020→2025, el tramo en que las dos fuentes se superponen. 2015→2025 va como secundaria, solo para comparar con el 02. Correlación de Spearman con `DataFrame.corr` (no requiere scipy).
- **Universo**: los 115 municipios con eventos, como se definió en el esqueleto. La tabla de correlaciones agrega, como referencia, el resultado con los 135, porque cambia bastante: 0,36 con 115 y 0,25 con 135.
- **Corrección respecto del esqueleto**: el "≈0,25" del esqueleto (y del texto que me pediste) lo había calculado con los 135 municipios. Con el universo acordado da 0,36, y el texto quedó con ese valor (ver §5.9). Lo mismo pasó con la correlación entre tasas: 0,94 con 135 y 0,90 con 115. El notebook usa 0,90.

### 2.18 Notebook 03: hash por archivo
- **Decisión** (acordada): el 03 lee tres archivos, así que la marca es `hash datos: exp=…;padron=…;serie=…` (`utils.hash_por_archivo`).
- **Comportamiento**: si cambia cualquiera de los tres, el control marca el markdown como "OK (hash de datos distinto: revisar; cambió: padron)", indicando cuál. Las marcas del 01 y el 02 (un hash único) siguen funcionando igual.

### 2.19 Notebook 04: cruce por código, no por nombre
- **Decisión**: `municipio_id` = "06" + `COD_MUNICIPIO` (3 dígitos, leído como texto). Coincide con los 135 ids del padrón en los dos sentidos. El nombre canónico se toma del padrón.
- **Motivo**: el código es unívoco. Por nombre había una variante nueva ("CORONEL DE MARINA L. ROSALES") y los nombres vienen en mayúsculas.
- **Alternativa descartada**: agregar la variante a `MUNICIPIOS_NORMALIZADOS`. Se descartó porque no hace falta y suma ruido al diccionario. Si en el futuro se necesita cruzar por nombre, hay que agregarla.

### 2.20 Notebook 04: ciclo → año
- **Decisión**: "2015-16" se mapea a `anio_inicio` = 2015, el año de la matrícula base del ciclo. La etiqueta original se conserva.
- **Superposición con el 02**: 9 ciclos (2015-16 a 2023-24); no hay 2024-25. El cruce compara el cambio de abandono con la variación de matrícula entre los mismos años base (2015 y 2023).
- **Superposición con el 03**: 4 ciclos (2020-21 a 2023-24). Solo entran los eventos de nivel secundario con acto entre 2020 y 2023. Se compara el **nivel** de abandono, no el cambio, porque el cambio desde 2020-21 estaría distorsionado por el ciclo atípico.
- **Con el 01**: no hay superposición temporal (abandono hasta 2023-24, padrón 2026). El cruce es estructural y se lee como asociación.

### 2.21 Notebook 04: valores negativos
- **Decisión** (acordada): se dejan como están, se marcan (columna `signo_ultimo`, color azul en los gráficos, escala divergente centrada en 0 en el heatmap) y los rankings usan medianas de varios ciclos.
- **Motivo**: la tasa es un residuo (100 − repitencia − reinscripción − promoción efectiva). Puede dar negativa cuando el municipio recibe más alumnos de los que pierde. Llevarlos a 0 sería corregir el dato.

### 2.22 Notebook 04: medidas por municipio
- **Principal**: mediana 2021-22 a 2023-24 (3 ciclos, sin 2020-21). **Secundaria**: promedio de esos ciclos. **Sensibilidad**: mediana 2020-21 a 2023-24.
- **Resultado**: los rankings son estables. Spearman da 0,87 entre la principal y la sensibilidad (13 de los 15 primeros se repiten) y 0,89 entre mediana y promedio.
- **Cambio en el tramo superpuesto**: el robusto (mediana 2021-24 menos mediana 2015-18) es el principal; el cambio entre extremos (2023-24 menos 2015-16) se muestra al lado.

### 2.23 Notebook 04: agregación por región
- **Decisión** (acordada): **principal**, la mediana de los municipios de cada región; **sensibilidad**, el promedio ponderado por la matrícula de Nivel Secundario del padrón 2026.
- **Limitación**: la matrícula del padrón 2026 no es la del ciclo 2023-24; es una aproximación, y el texto lo dice.
- **Resultado**: Spearman 0,82 en general, pero solo 2 regiones en común en los dos top 5. Por eso se muestran lado a lado: tabla y gráfico de puntos con las dos medidas por región.

### 2.24 Notebook 04: ciclo 2020-21
- **Decisión** (acordada): se muestra y se marca como atípico (punto y anotación en la serie, etiqueta en el heatmap).
- **Comparaciones**: la tabla de tramos reporta el tramo completo, antes de la pandemia (2010-11 → 2019-20), después (2021-22 → 2023-24), el salto y el rebote.
- **Rankings**: la medida principal lo excluye y la de sensibilidad lo incluye.

### 2.25 Notebook 05: cero cálculo y cifras para el informe
- **Decisión** (acordada): el 05 no recalcula. Las cifras que estaban solo en markdown o en prints de los notebooks 02 a 04 se guardaron en `outputs/0X_cifras_informe.csv` desde el notebook correspondiente. Cada fila tiene `cifra_id`, `valor`, `unidad`, `notebook`, `celda_origen` y `descripcion`.
  - `celda_origen` se completa automáticamente con el índice de la celda donde se calcula la cifra.
  - El pico (286 = 133 de 2022 + 153 de 2023) y el porcentaje rural (27,6 %; 9,4 + 18,1 da 27,5 por redondeo) llevan la aclaración en `descripcion`.
- **01 y CSV literales**: el 01 no necesitó archivo propio, porque sus cifras ya están literales en `01_totales.csv` y `01_distribucion_sector.csv`.
- **Lectura de los CSV**: el 05 lee los CSV por separado (`utils.leer_cifra`), sin un `05_cifras_informe.csv` que los una. Unirlos agregaba un archivo derivado más, sin ganar trazabilidad.
- **Única operación en el 05**: pasar alumnos a millones ("4,69 millones"), que es cambio de unidad, no cálculo.
- **Control en los notebooks de origen**: los controles de 01 a 04 siguieron dando OK después del agregado.

### 2.26 Notebook 05: publicación
- **HTML**:
  - Se genera con `nbconvert --no-input`, así que no muestra código.
  - Las celdas de configuración y de control llevan la etiqueta `ocultar` y se quitan con `TagRemovePreprocessor`; la tabla de control queda en `outputs/05_control_citas.csv`.
  - Los gráficos se muestran con texto alternativo (accesibilidad).
- **Imagen para LinkedIn**: `02_matricula_docentes_indice.png` (la misma de la portada, que no se repite en los hallazgos) centrado en un lienzo de 1200×630 (`utils.exportar_og_image`). Es procesamiento de imagen, no un gráfico nuevo.
- **Etiquetas Open Graph**: se insertan con reemplazo de texto (`utils.insertar_meta_og`). `og:title` es "Expansión y matrícula educativa en PBA, 2015–2026" (49 caracteres); el título completo queda en el `<title>` y en la portada.
- **Datos del autor y del repo**: se leen de `informe_config.json`, el único lugar a editar. Si quedan `[COMPLETAR]`, el script avisa y genera igual el HTML, para que se pueda revisar.
- **Sin dependencias nuevas**: solo nbconvert y matplotlib, que ya estaban.

## 3. Inconsistencias encontradas (no corregidas)

| Archivo | Columna | Problema | Casos | Ejemplo | Decisión |
|---|---|---|---|---|---|
| `establecimientos_educativos.csv` (descarga anterior) | todas | Archivo truncado a mitad de una fila: 490 filas, 6 municipios | 1 archivo | Última fila: establecimiento 479, Almirante Brown, nivel `"Ni"` y el resto vacío | Se reemplaza por la v2 y se conserva sin modificar como **referencia histórica**. Las 489 filas válidas están en la v2 con la misma matrícula |
| establecimientos (v2) | periodo | Valor "Nueva" en lugar de "Inicial 2026". **Inconsistencia documentada, no error**: son ofertas recién creadas | 115 | Matrícula 0 y secciones 0 en todas; 95 estatales y 20 privadas | Fuera de los conteos; reportadas en la sección 4 del 01 (§2.7) |
| establecimientos (v2) | establecimiento_id + nivel | No es clave única | 112 filas (56 pares) | 381 Alberti: Secundario Común + Técnico Profesional | Se usa `+ modalidad` (§2.2) |
| establecimientos (v2) | secciones | secciones = 0 en Educación Especial | 1.722 | — | Esperable; se deja |
| establecimientos (v2) | secciones | secciones = 0 con matrícula > 0, fuera de Especial | 3 | Plan FinEs (Trayectos y Deudores): Berazategui 580, José C. Paz 415 y 106 | Fuera de los conteos; reportadas (§2.7) |
| establecimientos (v2) | varones + mujeres vs. matrícula | — | 0 | — | Sin discrepancias. En el archivo viejo había 1 caso: la fila truncada |
| establecimientos (v2) | lat/long | Fuera del bounding box de PBA | 0 | — | — |
| establecimientos (v2) | modalidad | No existe "Agraria" como modalidad | — | Las EESA figuran en Técnico Profesional | §2.10 |
| **establecimientos (v2): auditoría del total** | matrícula | **Matrícula total del sistema = padrón − Nueva − FinEs sin secciones − CEF − CEC** = 4.878.699 − 0 − 1.101 − 158.857 − 28.017 = **4.690.724** | 5 restas | Padrón completo 4.878.699; "Nueva" 0 (115 ofertas); FinEs sin secciones 1.101 (3 ofertas); C.E.F. 158.857 (197 servicios); C.E.C. 28.017 (187 servicios) | Total oficial del informe. Se recalcula y se verifica con un `assert` en la sección 4 del 01 (`outputs/01_auditoria_matricula_total.csv`) |
| establecimientos (v2) vs. serie 2015–2025 | matrícula total | 4.690.724 (padrón Inicial 2026, matrícula del sistema) vs. 5.001.493 (serie, año 2025) | — | — | **No comparables**: el padrón es una foto por establecimiento al inicio de 2026; la serie es un agregado anual por municipio y región, con otra fecha de corte y posiblemente otra cobertura. No se cruzan; el 01 lo advierte en el cartel de alcance y en A2 |
| serie municipal 2015–2025 | municipio_nombre | 8 nombres distintos de los del padrón | 8 | "Veinticinco de Mayo" | Se normalizan (§2.3) y se conserva el original |
| serie municipios vs. regiones | docentes | La suma de municipios no coincide exactamente con la de regiones | 11 años, ≤ 2,6 cargos | 2020: −2,60 | Redondeo: decimales en municipios, enteros en regiones. Se deja |
| serie municipios vs. regiones | unidades, matrícula | — | 0 | — | Coinciden exactamente todos los años |
| serie regiones | docentes | Región 23: +44,5 % de cargos en 2025 | 1 | 8.793 → 12.705 | Se conserva; señalado en el 02 |
| serie municipal | matrícula | Mar Chiquita: pico de un solo año en 2023 | 1 | 9.362 (2022) → 12.734 (2023) → 9.936 (2024) | Dato real del relevamiento; se deja sin corregir. El 02 lo aclara en el markdown del heatmap. No afecta la variación 2015→2025 (+34,0 %) |
| establecimientos (v2) | matrícula de C.E.F. | Los Centros de Educación Física atienden alumnos ya matriculados en otra escuela: su "matrícula" son alumnos atendidos, no alumnos únicos | 197 CEF | 158.857 alumnos atendidos; 3 CEF habrían entrado en el top 10 | **Aplicado**: fuera de la suma de matrícula y en el análisis de oferta (§5.1) |
| establecimientos (v2) | matrícula de C.E.C. | Igual que los CEF: servicios complementarios sin matrícula propia | 187 CEC | 28.017 alumnos atendidos | **Aplicado**: mismo tratamiento (§5.2) |
| notebook 02, markdown `md-regiones` (texto, no dato) | unidades de servicio | El texto decía "20 de las 25" y "cinco" regiones en alza (1, 3, 5, 11 y 17); los datos dan 18 en baja y 7 en alza | 1 párrafo | — | **Corregido** en la segunda ronda con tu OK (§5.6) |
| notebook 01, markdown de La Plata (texto) | — | Dos textos que no cerraban con la v2 | 2 | "sistema educativo estatal"; "no se detectaron duplicados de id + nivel" | **Corregidos** en la segunda ronda con tu OK (§5.7) |
| expansión | fecha_acto | Años parciales en los extremos | 2 años | 2020 empieza el 23/04 (5 eventos); 2026 llega al 02/09 (31) | Se marcan como "(parcial)" en tablas y gráficos del 03 |
| expansión | resolucion | Nulos | 10 | — | Se dejan |
| expansión | establecimiento_id | Un establecimiento con dos eventos en el mismo año, creación y reapertura | 1 | 102873, EEP Nº33 de San Vicente: creación el 26/03/2021 (Resolución 1196) y reapertura el 05/08/2021 (Informe de la Secretaría de Inspección 89393) | Inusual; se documenta y no se corrige. Cuenta como 2 eventos (§2.14) |
| expansión vs. padrón | cueanexo | Eventos sin par en el padrón | 2 | CIIE "Mery Mouriz" de Lezama (2022; su CUI sí está en el padrón) y CIIE Nº 2 de Alberti (2025; ni CUI ni clave en el padrón) | Se reportan con una hipótesis cada uno (`outputs/03_eventos_sin_par_padron.csv`): el padrón no releva los CIIE. Verificado: no hay ningún CIIE en el padrón, ni por tipo de organización ni por nombre (el notebook lo controla con un `assert`). No se explica por el corte: ningún evento es posterior al 19/10/2026 |
| abandono | MUNICIPIO | Variante de nombre nueva | 1 | "CORONEL DE MARINA L. ROSALES" (código 182) | El dataset de abandono trae una variante nueva; se cruza por código y no se agrega al diccionario. Si en el futuro se necesita cruzar por nombre, agregarla. "PUAN" sin tilde ya era una variante conocida |
| abandono | VALOR | Nulo | 1 | Lezama 2010-11 | Lezama se separó de Chascomús en 2009. Queda fuera de la ventana de cruce (2015-16 a 2023-24); no afecta el análisis |
| abandono | VALOR | Valores negativos (la tasa es un residuo) | 124 (6,6 % de los 1.889 valores con dato) | 39 en 2020-21 y 21 en 2019-20; Monte Hermoso tiene 6; mínimo −8,1 | Se reportan y no se corrigen (`outputs/04_valores_negativos.csv`); los rankings usan medianas |
| abandono | VALOR | Ciclo atípico | 1 ciclo | 2020-21: 0,4 % provincial, contra 2,7 % y 2,8 % en los ciclos vecinos | Pandemia y promoción acompañada. Se muestra, se marca y se reporta con y sin él |
| abandono | VALOR | Cambio de precisión | 1 ciclo | 2023-24 con 2 decimales; los anteriores con 1 | No afecta las comparaciones (es redondeo, no dato) |
| expansión vs. padrón | periodo | Eventos cuyo establecimiento es una oferta "Nueva" (sin matrícula) | 24 | 16 de 2026, 5 de 2025 y **3 de 2023**: EEP N°99 (Lomas de Zamora), CFP N°404 (San Miguel) y CFL Nº405 (Florencio Varela) | Hallazgo para el 05. Los 3 de 2023 siguen sin matrícula casi tres años después (`outputs/03_nueva_2023_sin_matricula.csv`) |

## 4. Cambios de código relevantes

### `src/utils.py` (nuevo; ninguna de estas funciones existía antes, la lógica estaba repetida o inline en los notebooks)
- **Rutas**: `DATA_DIR = data/raw`, `OUTPUTS_DIR` y los nombres de archivo como constantes. Reemplazan las rutas repetidas y la ruta absoluta del 02.
- **Carga con tipos**: `cargar_establecimientos`, `cargar_expansion`, `cargar_matricula_municipios` (normaliza nombres) y `cargar_matricula_regiones`.
- **Municipios**: `MUNICIPIOS_NORMALIZADOS`, `normalizar_municipio`, `comparar_municipios`.
- **Calidad**: `resumen_nulos`, `chequear_clave_unica`, `chequear_genero`, `chequear_coordenadas`, `chequear_filas_incompletas` y `reporte_calidad_establecimientos`. Todos reportan, ninguno corrige.
- **Salidas y gráficos**: `guardar_figura`, `guardar_tabla`, `grafico_barras_h`, `aplicar_estilo`, `PALETA`, `CMAP_DIVERGENTE`, `formato_miles` (miles con punto), `separar_etiquetas` y `cagr`.
- **Control**: `hash_datos` y `verificar_citas` (parámetros `estricto` y `guardar_como`).

### Notebook 01
- **Eliminadas** (eran exploración del archivo truncado y quedaron reemplazadas por la sección 1 y la Parte A):
  - Celdas 2–13 y 15–21: shape, info, columns, value_counts, conteos por municipio y por nivel; varias repetidas entre sí.
  - Celdas 22–25: un primer filtro de La Plata, duplicado de la celda 27, y la exploración de la Región 1. El markdown de la celda 24 ("En la Región Educativa 1 solo aparecen La Plata y Berisso…") describía un efecto del corte y es falso con la v2.
  - Celda 28: `df_la_plata.info()`.
  - Celdas 30 y 31: duplicadas de las 35 y 36.
- **Reescritas**: la carga (ahora vía `utils`, con tipos) y el filtro de La Plata (ahora parte de `df_analisis`). En la celda 55 se sacó el comentario "# opcional, si querés…".
- **Conservadas tal cual**: el resto del análisis de La Plata (celdas 32–59), con sus textos. Solo se actualizaron números en los markdown 37, 42 y 60 (§2.9).
- **Gráficos nuevos**: 12 en total. Las 5 distribuciones, los 2 top 10, los 2 rankings de municipios, regiones, el mapa y La Plata por nivel y sector. El notebook original no tenía gráficos.

### Notebook 02
- **Eliminadas o fusionadas**:
  - Celdas 2–16 (exploración inicial): pasaron a la sección 1.
  - Celda 16: idéntica a la 18.
  - Celda 36: tenía una ruta absoluta `C:/Users/...`.
  - Celda 37: pasó a la sección 1.
  - Celda 99: repetía el `import`.
  - Celda 128: estaba contenida en la 129.
- **Variables renombradas** (antes se pisaban con significados distintos):
  - `comparacion` → `df_region_variacion` y `df_r23_vs_provincia`.
  - `comparacion_municipal` → `df_municipio_direccion` (por dirección del cambio) y `df_municipio_variacion` (variaciones % con trayectoria).
  - `la_plata` → `df_la_plata` y `fila_la_plata`.
  - `la_plata_anual` → `df_la_plata_anual`.
- **Markdown editados**:
  - Celda 23: se saca "Concepto que vas a aprender / El pivot()…" y se agrega la fórmula del CAGR.
  - Celda 59: "Recordá que…" → "La variable docentes…".
  - Celda 72: "ranking que compartiste" → "ranking anterior".
  - Celda 110: 42/92 invertido.
  - Celda 135: la URL de expansión pasa a una nota de "fuera de alcance".
  - Celda 28 (Región 23): al releerla, la frase original era correcta y **no se modificó**. En el diagnóstico la había marcado como ambigua por error.
- **Gráficos**: los 7 existentes pasaron a `fig, ax` explícitos, con colores de la paleta, fuente y guardado. Se suman 5 nuevos.

### Segunda ronda (correcciones aprobadas)
- **02**:
  - Markdown `md-regiones`: corrección del párrafo de unidades (§5.6).
  - Markdown del heatmap: ahora lleva marca `md-heatmap` y la nota sobre Mar Chiquita.
  - Celda de control: +15 verificaciones (8 listas, 4 cifras nuevas del párrafo corregido y 3 de Mar Chiquita) y −1 (el "En 20" viejo).
- **01**:
  - Markdown 46: "estatal y privado".
  - Markdown 60 (`md-lp-resumen`): texto sobre el 10474.
  - Markdown del top 10 de Secundario: aclaración sobre las agrarias.
  - Se eliminaron las dos notas [REVISAR] que había agregado, porque ya no hacen falta.
  - Celda de control: +2 verificaciones.
- **utils.py**: `verificar_citas` acepta conjuntos como valor calculado (`_comparar_conjunto`).
- **backup/originales/**: copia sin procesar de los dos notebooks anteriores a la revisión.

### Criterio de simplificación de solapamientos
Sirve para que, al integrar en el 05, se sepa qué está duplicado **a propósito** y no se "corrija" de nuevo. No reabre nada. Los números de celda son los de los notebooks finales (índice 0, como en el `.ipynb`).

**Criterio**
- **Redundancia evitable** → se simplifica. Recalcular una métrica ya calculada, mostrar tabla y gráfico de lo mismo, o reagrupar lo que ya está agregado.
- **Redundancia intencional** → se conserva. La misma información vista de otra forma o en otro universo, con un propósito distinto (explicar una exclusión en el lugar donde se ve, verificar un total por dos caminos, contar establecimientos frente a ofertas, etc.).

**Redundancia evitable: simplificada**

| Notebook | Caso | Qué se hizo | Celda final |
|---|---|---|---|
| 01 | Original 30 y 31 (establecimientos de La Plata por nivel y por modalidad) repetían las 35 y 36 | Se eliminaron | 63 y 64 |
| 01 | Original 22 (filtro de La Plata) repetía la 27 | Se eliminó | 60 |
| 01 | Originales 18–20 ("niveles por establecimiento" y dos veces "establecimientos por nivel") | Se reemplazaron por una sola celda | 27 (A1) |
| 01 | Originales 2–13 y 15–21 (exploración repetida sobre el archivo truncado) | Se reemplazaron por la sección 1 | 4–23 |
| 02 | Original 16 (totales por año) idéntica a la 18 | Se eliminó | 20 |
| 02 | Original 128 (extremos de unidades) contenida en la 129 | Se eliminó | 144 |
| 02 | Originales 2–15 y 37 (exploración de forma, tipos, nulos y duplicados) | Se consolidaron en la sección 1 | 3–17 |
| 02 | Original 99: `import` repetido | Se eliminó | — |

**Redundancia evitable: NO simplificada** (se conservó porque es tu análisis y tus markdown citan cada salida; queda señalada para el 05)

| Notebook | Caso | Celdas |
|---|---|---|
| 02 | La variación de matrícula 2015→2025 por municipio se calcula **tres veces** con el mismo resultado: `matricula_cambio`, `matricula_extremos` y `variaciones_absolutas` (esta última agrega el cambio absoluto) | 48, 100, 118 |
| 02 | El conteo de municipios que aumentaron o disminuyeron su matrícula aparece dos veces | 50, 104 |
| 02 | Rankings municipales repetidos: top 5 absolutos, top 5 %, top 10 absolutos y top 10 % | 52, 117, 121, 137 |
| 02 | **Agregada por mí**: el top 10 % que crece y que cae repite el de la celda 137. Suma CAGR y exporta CSV, pero los municipios son los mismos | 58 |
| 02 | La dirección del cambio matrícula × unidades se clasifica dos veces: tabla cruzada de 3×3 y trayectoria de 9 categorías (la segunda contiene a la primera) | 63/65, 114/134 |

**Redundancia intencional: conservada**

| Notebook | Caso | Propósito | Celdas |
|---|---|---|---|
| 01 | Nota al pie del top 10 (`md-top10-nota`) que repite los 3 CEF listados también en la sección 4 | Explicar la exclusión justo donde se ve el ranking | 47–48 (nota) y 100 (sección 4) |
| 01 | Total en A2 y auditoría del total en la sección 4 | El mismo total calculado por dos caminos (suma de `matricula_sistema` y padrón menos cada resta), con `assert` de igualdad | 31 y 101–102 |
| 01 | Sección 4 (auditoría) y sección 5 (control de cifras) | La 4 verifica los **datos**; la 5 verifica los **textos** contra los datos | 92–102 y 103–104 |
| 01 | `nunique` frente a `value_counts` en La Plata | `nunique` cuenta establecimientos únicos y `value_counts` cuenta ofertas (filas); dan números distintos a propósito | 63–65 y 67 |
| 01 | Niveles por establecimiento, provincia y La Plata | Misma métrica, distinto universo | 27 y 69 |
| 01 | Distribuciones por nivel, modalidad y sector, provincia y La Plata | Misma métrica, distinto universo (Parte A y Parte B) | 35–44 y 63–65 |
| 02 | Regiones: tabla, gráfico de variación y top 5 | Tres vistas con tres propósitos: la tabla tiene todos los valores y se exporta, el gráfico compara las 25 regiones de un vistazo, y el top 5 muestra la trayectoria anual | 31, 33 y 35 (texto en 36) |
| 02 | Totales por año, variación y tabla de variación + CAGR | La tabla final consolida para exportar y agrega CAGR; no recalcula | 20, 22 y 24 |
| 01 y 02 | Chequeo de nombres de municipio en los dos notebooks | Cada notebook se puede ejecutar solo | 01: 19 · 02: 14 |
| 01 y 02 | Celda de control de cifras en los dos | Misma lógica (`utils.verificar_citas`); cada una controla sus propios textos | 01: 104 · 02: 152 |
| 01 y 02 | Totales de matrícula en los dos notebooks | **No es un solapamiento**: son mediciones distintas (padrón 2026 y serie 2015–2025), no comparables (§3) | 01: 31 · 02: 20 |

### Tercera ronda (C.E.F. y C.E.C.)
- **01**:
  - Cartel de alcance: nueva viñeta "Matrícula del sistema".
  - Universo de análisis: regla de `matricula_sistema` en el markdown; en el código, la constante `SERVICIOS_SIN_MATRICULA_PROPIA` y las columnas `matricula_sistema` y `alumnos_atendidos_servicios`.
  - A2: el total pasa a "matrícula del sistema", con una fila aparte para los alumnos atendidos.
  - A3: `tabla_distribucion` suma `matricula_sistema` y agrega `atendidos_servicios`; los gráficos omiten las categorías con matrícula 0.
  - A4: el ranking usa `matricula_sistema`. Se agregan una celda y una nota al pie (`md-top10-nota`) con los 3 CEF que salieron.
  - A5, A6 y Parte B (apertura por sector, gráfico nivel × sector y tus celdas 47, 48, 53 y 55): sumas con `matricula_sistema`. Las estadísticas por fila (`describe`, media 260 / mediana 160) siguen sobre `matricula`, porque describen ofertas, no el total.
  - Sección 4: subsección de servicios (`md-servicios`), verificación por CUI y por municipio (con `assert`), top 10 de servicios y auditoría del total (`md-auditoria-total`).
  - Control: +11 verificaciones (32 en total).
- **02**: sin cambios.

### Notebook 03 (nuevo) y cambios en utils.py
- **utils.py**:
  - `hash_por_archivo`.
  - `preparar_padron_analisis`: el universo del padrón con `matricula_sistema`, con el mismo criterio que el 01. **Unificado antes del 05**: el 01 ahora usa la función de `utils`, con un `assert` que verifica que da las mismas filas que sus máscaras de exclusión. Regresión: los 20 CSV `outputs/01_*` quedaron **idénticos byte a byte** y el control siguió en 32/32 OK.
  - `SERVICIOS_SIN_MATRICULA_PROPIA` como constante compartida y `FUENTE_EXPANSION`.
  - La regex de la marca de verificación acepta el formato `exp=…;padron=…`, y el aviso de hash distinto dice qué archivo cambió.
  - Se volvieron a ejecutar el 01 y el 02 después de estos cambios: siguen dando 32/32 y 183/183 OK.
- **Notebook 03**: 65 celdas, 7 gráficos y 14 CSV con prefijo `03_`.

### Notebook 04 (nuevo) y cambios en utils.py
- **utils.py**:
  - `cargar_abandono()` devuelve `(municipios, total_provincia)`, con `municipio_id` y `anio_inicio` ya calculados, y el total provincial (código `CODIGO_TOTAL_PROVINCIA` = "000") separado.
  - Constantes `ARCHIVO_ABANDONO` y `FUENTE_ABANDONO`.
  - Se volvieron a ejecutar el 01, el 02 y el 03: siguen dando 32/32, 183/183 y 82/82 OK.
- **Notebook 04**: 55 celdas, 6 gráficos y 12 CSV con prefijo `04_`. Los textos interpretativos se escribieron después de una primera corrida, con las cifras del propio notebook, para no repetir el desfase entre perfilado y notebook del 03.

### Notebook 05 (nuevo) y cambios para el informe
- **02, 03 y 04**: una sección "Cifras para el informe de síntesis" antes del control, que guarda `0X_cifras_informe.csv` (14, 15 y 15 cifras). Sus controles siguen en 183, 82 y 78 OK.
- **utils.py**:
  - `guardar_cifras_informe`, `leer_cifra`, `hash_outputs`, `exportar_og_image` e `insertar_meta_og`.
  - El hash del 05 cubre los cuatro archivos de datos y los CSV de `outputs/` que lee (`…;outputs=…`).
- **Archivos nuevos**:
  - `src/publicar_informe.py`: ejecuta el 05, exporta el HTML, arma la imagen e inserta las etiquetas.
  - `informe_config.json`: autor, usuario de GitHub, LinkedIn, títulos y descripción para LinkedIn.
  - `docs/`: la salida publicable.
- **Las 5 redundancias evitables no simplificadas del 02** quedan como están; el 05 usa una sola fuente por cifra (los CSV de `outputs/`), y esta sección indica cuál es la fuente canónica para el informe. Fuentes canónicas del 05:
  - Matrícula 2015–2025 y regiones: `02_cifras_informe.csv`.
  - Top municipales: `02_cifras_informe.csv`, que sale de `df_municipio_ranking`, celda 58 del 02.
  - Estructura del sistema: `01_totales.csv` y `01_distribucion_sector.csv`.
  - Expansión: `03_cifras_informe.csv` y `03_pico_2022_2023_por_tipo.csv`.
  - Abandono: `04_cifras_informe.csv`.

### `requirements.txt` (nuevo)
- Versiones exactas del `.venv` donde se probó: pandas, openpyxl (lectura de los xlsx), matplotlib, seaborn (stripplot y heatmap del 02), numpy (`np.sign`, `np.select`, `np.ceil`), jupyter, nbconvert e ipykernel (para ejecutar desde la línea de comandos).

## 5. Supuestos

No quedan supuestos [REVISAR] abiertos para 01 a 04. Los que se marcaron durante la revisión están todos resueltos, con la decisión tomada.

### 5.1 [RESUELTO] C.E.F. (Centros de Educación Física): fuera de la matrícula total
- **Decisión**: los CEF se excluyen de la matrícula total del sistema porque no tienen matrícula propia asignada; su matrícula es de alumnos atendidos que ya están matriculados en otra escuela. Se **mantienen en el análisis de oferta**: son 197 establecimientos reales y siguen contando como establecimientos, ofertas y secciones. En el notebook se implementa con la columna `matricula_sistema`, que vale 0 en los CEF y CEC; la columna `matricula` original no se toca.
- **Impacto**: matrícula total **4.877.598 → 4.718.741 (−158.857)**. Al sumar la exclusión de los C.E.C. (§5.2), el total final queda en **4.690.724**. Salen tres CEF del top 10 de establecimientos; quedan listados en la nota al pie del ranking (`outputs/01_top10_servicios_excluidos.csv`):
  - CEF Nº1 de General Pueyrredón: 4.629 alumnos atendidos.
  - CEF Nº 2 "Maestro Isauro Arancibia" de La Plata: 3.488.
  - CEF Nº123 "Jorge Newbery" de Tres de Febrero: 3.335.

  La matrícula de La Plata pasa de 241.291 a 237.803.
- **Limitación de la verificación**: la prueba por CUI no es concluyente; el criterio se sostiene por la comparación por municipio.
  - *Por CUI*: 68 de 197 CEF comparten edificio con otro establecimiento. En 33 la matrícula del CEF supera a la del edificio y en 35 no. Un CEF atiende a alumnos de muchas escuelas, no solo de las de su edificio, así que esta prueba no discrimina.
  - *Por municipio*: en **0 de 134** municipios la matrícula de los CEF supera a la de primaria + secundaria (mediana 12,25 %, máximo 75,6 % en Tordillo).
  - En la segunda ronda reporté 69 y 34. La diferencia es que ahora los establecimientos del mismo edificio se cuentan **sin** los C.E.C.
- **Auditable en**: `outputs/01_verificacion_servicios_cui.csv` (un registro por servicio, con la matrícula de su edificio) y `outputs/01_verificacion_servicios_municipio.csv` (servicio contra primaria + secundaria, por municipio). Los regenera la sección 4 del notebook 01. Esa sección tiene un `assert` que falla si algún servicio llegara a superar a primaria + secundaria de su municipio.

### 5.2 [RESUELTO] C.E.C. (Centros Educativos Complementarios): mismo tratamiento que los CEF
- **Decisión**: igual que los CEF. Son servicios complementarios que atienden a alumnos matriculados en escuelas comunes (apoyo escolar, talleres). Se excluyen de la matrícula total del sistema y se mantienen en el análisis de establecimientos.
- **Verificación** (mismo método que los CEF; los números son similares, así que se aplicó):
  - Ninguno de los 187 CEC comparte `establecimiento_id` con otra oferta.
  - *Por CUI*: 25 de 187 comparten edificio; en 11 el CEC supera a su edificio y en 14 no. No es concluyente, por la misma razón que en los CEF.
  - *Por municipio*: en **0 de 108** municipios superan a primaria + secundaria (mediana 2,55 %, máximo 24,2 % en Guaminí).
- **Impacto**: matrícula total **4.718.741 → 4.690.724 (−28.017)**. Ningún CEC estaba en el top 10: el de mayor matrícula tiene 319 alumnos atendidos. La Plata no tiene CEC.

### Servicios que no aportan matrícula propia

| Servicio | Cantidad | Alumnos | Tratamiento |
|---|---|---|---|
| C.E.F. (Educación Física) | 197 servicios | 158.857 alumnos atendidos | En la oferta; no se suman a la matrícula |
| C.E.C. (Centros Educativos Complementarios) | 187 servicios | 28.017 alumnos atendidos | En la oferta; no se suman a la matrícula |
| Ofertas "Nueva" | 115 ofertas | 0 alumnos | Fuera de los conteos; reportadas aparte |
| FinEs sin secciones | 3 ofertas | 1.101 alumnos | Fuera de los conteos; reportadas aparte |

Estos servicios se reportan en el análisis de oferta pero no se suman a la matrícula total del sistema, para evitar doble conteo. Las "Nueva" y las FinEs sin secciones, además, quedan fuera de los conteos de ofertas y establecimientos (§2.7).

### 5.3 [RESUELTO] Ofertas "Nueva" fuera de los conteos
- **Decisión** (segunda ronda): se excluyen de conteos y análisis y se reportan aparte en la sección 4 del 01 (cantidad, nivel × modalidad, top 10 municipios). Tienen matrícula 0 y secciones 0; dejarlas distorsionaría los promedios de matrícula por establecimiento.
- **Impacto**: −115 ofertas en los conteos; matrícula sin cambios.

### 5.4 [RESUELTO] FinEs sin secciones fuera de los conteos
- **Decisión** (segunda ronda): las 3 filas de Plan FinEs con secciones = 0 y matrícula > 0 tienen el mismo tratamiento que las "Nueva": quedan fuera de los conteos y se reportan aparte.
- **Impacto**: −1.101 alumnos y −3 ofertas.

### 5.5 [RESUELTO] Definición de Nivel Secundario para el top 10
- **Decisión**: Educación Común + Educación Técnico Profesional, según tu pedido ("Común + Técnico Profesional + Agraria"). Las escuelas agrarias figuran como Técnico Profesional en el padrón, así que están incluidas, y el notebook lo aclara. Quedan fuera CENS (89.211) y Artística (4.384).
- **Cómo cambiarlo**: editar `MODALIDADES_SECUNDARIO` en el 01.

### 5.6 [RESUELTO] Texto del 02 sobre unidades de servicio por región
Decía "En 20 de las 25…" y "Cinco regiones…: 1, 3, 5, 11 y 17". Ahora dice: "Entre 2015 y 2025, las unidades de servicio bajaron en 18 de las 25 regiones y subieron en 7: las Regiones 1, 3, 5, 10, 11, 17 y 18. La Región 10, por ejemplo, pasó de 902 a 924 unidades (+2,44 %)." El control verifica la cantidad, la lista completa y las cifras de la Región 10.

### 5.7 [RESUELTO] Textos de La Plata que dejaron de cerrar
- La pregunta ahora dice "¿cuánta matrícula hay realmente en el sistema educativo **estatal y privado** registrado de La Plata?".
- El resumen final ahora dice: "No se detectaron duplicados exactos. Sí hay 1 caso que repite la clave establecimiento_id + nivel en las 927 filas: el establecimiento 10474 (Escuela Técnica San Vicente de Paul, privada), que tiene Nivel Secundario en dos modalidades (Común y Técnico Profesional). Es el mismo fenómeno que el establecimiento 381 de Alberti: la clave única real es establecimiento_id + nivel + modalidad." El control verifica el "1 caso" y el id 10474.

### 5.8 Mar Chiquita 2023 (sin cambios)
Es un dato real del relevamiento: se deja documentado y sin corregir (§3). El 02 lo aclara en el markdown del heatmap.

### 5.9 [RESUELTO] Notebook 03: universo y adjetivo de la correlación expansión–matrícula
- **Decisión**: el universo principal son los **115 municipios con eventos**, y los 135 van como sensibilidad. Los 20 municipios sin eventos no informan sobre la relación entre expansión y matrícula: sus ceros significan "no hay eventos en este archivo", no "no hay relación". El adjetivo queda **"débil a moderada"** (Spearman 0,36 con 115 casos: es una asociación real, pero no fuerte).
- **Origen**: el "≈0,25" del esqueleto venía de mi perfilado con 135 municipios. En el párrafo de San Vicente, los "3.545 alumnos" del esqueleto contaban dos veces al 102873 (227 alumnos); contando cada establecimiento una vez son **3.318**.

### 5.10 [RESUELTO] Notebook 03: interpretación de la diferencia entre 0,36 y 0,25
- **Decisión**: queda la redacción propuesta (markdown `md-correlacion` del 03), más una línea aparte sobre la diferencia entre grupos.
- **Por qué se descartaron las frases originales** (para no volver a ellas sin revisar):
  - *"Los municipios sin expansión registrada tienen, en promedio, menor crecimiento de matrícula"*: lo contradice la variación 2020→2025 de los 20 sin eventos, que es similar a la de los 115 con eventos (media +0,55 % contra +0,02 %; mediana −1,14 % contra −1,16 %).
  - *"La expansión se concentra donde ya había crecimiento"*: lo contradice que la intensidad de la expansión no se asocia con el crecimiento previo 2015→2020 (Spearman −0,03 en los 115 municipios).
- **Qué explica la diferencia entre 0,36 y 0,25**: los 20 municipios sin eventos entran todos con tasa 0 y con un crecimiento repartido como el del resto, y eso diluye la asociación.
- **Hallazgo descriptivo que sí se sostiene**, agregado como línea aparte en el texto: "Los municipios con algún evento venían creciendo más antes de 2020 (+4,63 % en 2015→2020 contra +1,81 % en los sin eventos), pero esa diferencia es entre grupos, no según la intensidad de la expansión."
- **Evidencia auditable**: `outputs/03_crecimiento_con_sin_eventos.csv` y la celda correspondiente del notebook. El control verifica todas las cifras del párrafo.

### 5.11 [RESUELTO] Notebook 04: porcentaje de valores negativos
- En el perfilado te había dicho "124 negativos (6,5 %)". Ese 6,5 % estaba calculado sobre las 1.904 filas, incluidos el total provincial y el nulo. Sobre los 1.889 valores municipales con dato es **6,6 %**, y el texto del 04 usa ese valor. Los 124 casos, los 39 de 2020-21, los 21 de 2019-20 y los 6 de Monte Hermoso no cambian.

### Supuestos declarados (sin decisión pendiente)
- **"Docentes" son cargos, no personas** (02). Es el criterio de tu notebook original y está explicado en su texto: "los cargos no equivalen a personas". Afecta toda razón "matrícula por docente".
- **La v2 es la versión vigente y está completa**. Verificado: 135 municipios, 25 regiones, termina en un salto de línea, sin filas incompletas, y las 489 filas válidas del archivo viejo coinciden.
- **Los demás servicios tienen matrícula propia**: Formación Integral, Formación Profesional, Cursos y Talleres, Ciclo Medio y Ciclo de Iniciación se suman a la matrícula. No los verifiqué con el método de CEF/CEC porque, a diferencia de esos dos, son ofertas formativas con alumnos inscriptos propios. Si querés confirmarlo, el método de la sección 4 del 01 se aplica agregando el nivel a `SERVICIOS_SIN_MATRICULA_PROPIA`.

## 6. Pendientes y preguntas abiertas
- `informe_config.json` ya está completo (autor, usuario de GitHub, LinkedIn y URL de GitHub Pages) y `docs/index.html` está regenerado con esos datos.
- `notebooks/evolucion_interactiva.html` (gráfico Plotly de matrícula y cargos docentes en La Plata, del 12/10) se borró: era un experimento anterior a la revisión, no lo generaba ningún notebook y su contenido está en `outputs/02_la_plata_evolucion.png`.
- **Publicar en GitHub Pages**: ver §7.
- Opcional: confirmar con la fuente que FinEs sin secciones, el pico de Mar Chiquita en 2023, los 2 CIIE sin par y el doble evento del 102873 son propios del relevamiento (ya están documentados).
- Las 5 redundancias evitables no simplificadas del 02 quedan señaladas (§4); no afectan al informe.
- Posibles extensiones, fuera del alcance de este proyecto: el ciclo 2024-25 de abandono cuando se publique, y otros indicadores de trayectoria (repitencia, sobreedad).

## 7. Cómo reproducir
1. Entorno: Python 3.14.7. `python -m venv .venv` y luego `.venv\Scripts\pip install -r requirements.txt`.
2. Datos en `data/raw/` (no se modifican): `establecimientos-educativos-19102026.csv`, los dos xlsx de la serie 2015–2025 `expansion-sistema-educativo-21092026.csv` y `11_tasa_de_abandono_del_nivel_secundario.xlsx`. El archivo truncado `establecimientos_educativos.csv` solo se usa para la comparación del 01.
3. Orden de ejecución: los notebooks son independientes (el 03 lee los datos crudos, no los outputs del 01 ni del 02); se sugiere 01, 02, 03, 04. Desde la raíz del proyecto:
   ```
   .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks/01_establecimientos_educativos.ipynb
   .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks/02_matricula_2015_2025.ipynb
   .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks/03_expansion.ipynb
   .venv\Scripts\jupyter nbconvert --to notebook --execute --inplace notebooks/04_abandono_secundario.ipynb
   .venv\Scripts\python src\publicar_informe.py
   ```
   El último comando ejecuta el 05 y genera `docs/index.html` y `docs/og-image.png`.
   Si algún día la celda de control falla, nbconvert aborta y no guarda los outputs. Para inspeccionar el problema, poné `MODO_ESTRICTO = False` o agregá `--allow-errors`. La tabla de control se guarda igual en `outputs/`.
4. Todos los PNG y CSV se regeneran en `outputs/`.
5. Las versiones originales de los notebooks, anteriores a esta revisión, están en `backup/originales/` como referencia. No se procesan.
6. **Publicar en GitHub Pages**:
   1. Verificar `informe_config.json` y volver a correr `src/publicar_informe.py` si cambió algo.
   2. Crear el repositorio `informe-educacion-bonaerense` en GitHub y subir el proyecto (incluida la carpeta `docs/`).
   3. En el repositorio: *Settings → Pages → Build and deployment → Source: Deploy from a branch*, rama `main` y carpeta `/docs`.
   4. En uno o dos minutos el informe queda en `https://NicolasLascours.github.io/informe-educacion-bonaerense/`.
   5. Antes de compartir, conviene revisar la vista previa con el Post Inspector de LinkedIn (`https://www.linkedin.com/post-inspector/`).
