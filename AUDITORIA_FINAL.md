# Auditoría final del proyecto

> **Nota:** esta auditoría se hizo el 23/10/2026, antes de las correcciones finales. Los críticos C1, C2 y C3 y las advertencias esenciales están resueltos en la versión publicada. Se conserva como registro del proceso de revisión.

Fecha: 23/10/2026. Revisión de solo lectura: no se corrigió nada. Lo único que se modificó fue lo que regenera la re-ejecución de los cinco notebooks (los CSV de `outputs/` quedaron idénticos byte a byte a los anteriores).

## 1. Resumen ejecutivo

- 🟢 **Datos y cálculos**:
  - Los cinco archivos de entrada están, se leen y sus hashes coinciden con las marcas de verificación.
  - Los cinco notebooks corren en modo estricto sin errores (01 32/32, 02 183/183, 03 82/82, 04 78/78 y 05 77/77 OK), con las mismas cantidades de verificaciones que la última corrida.
  - Las cifras compartidas entre notebooks coinciden.
- 🟢 **outputs/**: 96 archivos (37 PNG y 59 CSV), todos válidos y todos generados por algún notebook. El 05 lee 15 y no le falta ninguno.
- 🔴 **docs/ (informe publicable)**: el HTML tiene 4 `[COMPLETAR]` visibles y los enlaces al repositorio, a la documentación, a LinkedIn y a la imagen de vista previa están rotos (§2, C1).
- 🟡 **Textos del notebook 02**: dos frases tuyas contradicen la serie de datos (§2, C2 y C3). No están en el informe 05, pero el notebook se publica en el repo.
- 🟡 **Presentación y repo**: el HTML no es responsive en celulares, el repo no tiene `.gitignore` ni `README.md`, y hay inconsistencias de datos sin documentar (§3).

## 2. CRÍTICOS

| # | Qué | Dónde | Detalle | Cómo se corrige |
|---|---|---|---|---|
| C1 | **El informe tiene `[COMPLETAR]` y enlaces rotos** | `docs/index.html`, `informe_config.json` | 4 `[COMPLETAR]` visibles (autor en portada y footer, entre otros). Los enlaces rotos son: el del repositorio y el de `DOCUMENTACION.md` (`https://github.com/%5BCOMPLETAR%5D/...`), el de LinkedIn (enlace relativo `%5BCOMPLETAR%5D`) y las URL de `og:image` y `og:url`, así que la vista previa en LinkedIn no va a mostrar la imagen | Completar `autor`, `usuario_github` y `linkedin` en `informe_config.json` y correr `.venv\Scripts\python src\publicar_informe.py` |
| C2 | **Texto que contradice la serie** | Notebook 02, celda 126 (`md-conclusiones`), redacción tuya | Dice: "alcanzó su máximo en 2019 y luego descendió durante los años siguientes, **con una recuperación hasta 2023** y nuevas disminuciones en 2024 y 2025". Los datos: 2019 5.218.472 → 2020 5.138.086 → **2021 5.159.560 (único año de suba)** → 2022 5.149.536 → 2023 5.124.691 → 2024 5.052.747 → 2025 5.001.493. No hay recuperación hasta 2023: hay un repunte solo en 2021 | Cambiar por algo como "con un leve repunte en 2021 y bajas desde 2022". El control no lo detecta porque la frase no tiene cifras |
| C3 | **Texto que contradice el dato** | Notebook 02, celda 98 (`md-lp-sintesis`), redacción tuya | Dice que la matrícula por unidad de servicio de La Plata "**alcanzó su máximo en 2024** y descendió en 2025". El máximo es **2023** (275,99, contra 275,91 en 2024). La diferencia es mínima, pero el texto no coincide | Cambiar "2024" por "2023" (o "en 2023–2024", si se quiere marcar que son casi iguales) |

C1 bloquea la publicación del HTML. C2 y C3 no afectan al HTML del 05 (que no cita esas frases), pero son errores de texto en un notebook que va al repo.

## 3. Advertencias

**Presentación del informe (docs/)**
- **A1. No es responsive en celulares**: el HTML no tiene `<meta name="viewport">` (el template de nbconvert no lo incluye). En un teléfono la página se renderiza con ancho de escritorio y se ve achicada. Las imágenes tienen `max-width:100%`, pero el texto queda chico. Como la audiencia de LinkedIn es mayormente mobile, conviene agregar la etiqueta en el mismo paso que inserta las og (`insertar_meta_og`).
- **A2. No es 100 % autocontenido**: carga `require.js` y MathJax desde cdnjs. Funciona en línea y el informe no usa fórmulas, así que MathJax sobra; se puede desactivar en la exportación.
- **A3. El footer no enlaza al catálogo de datos**: dice "Datos abiertos de la Provincia de Buenos Aires" sin enlace. Los cuatro datasets están enlazados en la portada.
- **A4. Hallazgo 5 sin la ventana de comparación**: "112 de los 135 municipios bajaron su abandono" no dice entre qué ciclos. En el 04 es entre la mediana 2015-16 a 2017-18 y la mediana 2021-22 a 2023-24.
- **A5. El título dice 2015–2026, pero el hallazgo 5 cubre desde 2010-11**: o se aclara en el subtítulo, o el título pasa a "2010–2026".
- **A6. La misma imagen aparece dos veces**: el gráfico de abandono está en la portada (imagen destacada) y en el hallazgo 5. Puede ser intencional; si no, en la portada podría ir otra.
- **A7. Detalles de redacción menores**:
  - El hallazgo 1 menciona la exclusión de CEF y CEC, pero no la de "Nueva" (0 alumnos) ni la de FinEs sin secciones (1.101 alumnos).
  - "Una baja desde entonces" (resumen) pasa por alto el repunte de 2021.
  - La viñeta 6 del resumen no repite universo y ventana (sí están en el hallazgo 6).

**Repositorio**
- **A8. No hay `.gitignore`**: un `git add .` subiría el `.venv` completo (530 MB, 25.823 archivos; ninguno supera los 100 MB, así que el push no fallaría, pero inflaría el repo) y las carpetas `__pycache__`.
- **A9. No hay `README.md`**: GitHub mostraría el repo sin portada. Hoy el punto de entrada es `DOCUMENTACION.md`.
- **A10. Texto desactualizado**: notebook 02, celda 150: "Queda pendiente un posible `03_expansion.ipynb`". El 03 ya existe.
- **A11. Archivo suelto**: `notebooks/evolucion_interactiva.html` (4,8 MB, del 12/10, anterior a esta revisión). No lo genera ningún notebook ni lo referencia nadie (ver §6).
- **A12. `informe_config.json` no tiene `url_github_pages`**: no es un error, porque la URL se arma con `usuario_github` y `repo`, pero mencionaste ese campo.

**Calidad de datos no documentada en §3 de DOCUMENTACION.md**
- **A13. Matrícula por sección atípica**: 30 ofertas con más de 60 alumnos por sección, casi todas de educación de adultos privada. La peor es el Instituto Dr. Mariano Moreno (Quilmes): 2.223 alumnos en 3 secciones. Puede ser modalidad a distancia o error de carga. No afecta ninguna cifra publicada.
- **A14. Saltos de un año en la serie municipal de matrícula**, además del de Mar Chiquita, que sí está documentado: hay 21 saltos interanuales de más del 15 %, varios con rebote al año siguiente (Leandro N. Alem 2020/2021, Tornquist 2017/2018, Monte Hermoso 2016/2017, Dolores 2018/2020, General Lavalle 2023/2024).
- **A15. Saltos fuertes en la serie de docentes**: 19 variaciones interanuales de más del 40 %. Daireaux 2025 da +207,5 %, Carlos Casares 2018 +113 % y General Alvear 2023 +108 %. El 02 ya pedía revisar los saltos de la Región 23 y de La Plata; estos se suman.

**Lo que se verificó y está bien**
- El archivo truncado sigue en `data/raw/` y solo lo usa la celda de comparación del 01.
- `og:title` tiene 49 caracteres y `og:image` apunta a `og-image.png`. La imagen mide 1200×630 y se lee bien.
- No se ve código (`--no-input`) ni la sección de control (etiqueta `ocultar`). Las 7 imágenes están embebidas (base64) y tienen texto alternativo.
- `requirements.txt` coincide exactamente con lo instalado en el `.venv`.
- Los comandos de §7 que ejecutan los notebooks y el script de publicación funcionan. No se probó crear un `.venv` nuevo ni `pip install`, para no modificar el entorno.

## 4. Huecos de análisis

| # | Hueco | Tipo | Dónde iría | Prioridad |
|---|---|---|---|---|
| H1 | **Cargos docentes**: el 02 los calcula (tabla provincial, Región 23, La Plata), pero el 05 no los menciona y tampoco están en la lista de "lo que quedó fuera". Crecieron +20,2 % contra +1,78 % de matrícula (ver hallazgo nuevo 1) | Hueco real (olvido, no decisión) | 05, como contexto del hallazgo 2, con cifras en `02_cifras_informe.csv` | Alta |
| H2 | **Revisión de los saltos de cargos docentes**: el 02 dice "merecen una revisión específica" (celdas 36, 45, 77 y 126) y no se hizo. A15 suma 19 saltos más | Hueco real, pero requiere información externa (metodología de la fuente) | DOCUMENTACION §6 como pendiente con la fuente; no es análisis | Media |
| H3 | **Por qué y dónde bajó más el abandono**: el 04 tiene dónde (mayores bajas y subas municipales) y el 05 no lo trae. El porqué no se analiza en ningún lado | El dónde es decisión (está en el 04). El porqué está fuera de alcance, pero no está dicho explícitamente en el 05 | Una línea en la conclusión del 05 ("el informe no analiza causas") | Baja |
| H4 | **Columnas del padrón sin usar**: ver lista abajo | Decisión de alcance, salvo `area` (útil) | `area` en 02 y 03; el resto no va | Media (`area`) / baja (resto) |
| H5 | **Cortes temporales sin cruce**: la matrícula 2024–2025 no tiene abandono (el dataset termina en 2023-24); la expansión 2024–2026 no tiene abandono; el abandono 2010-11 a 2014-15 no tiene serie de matrícula | Decisión de alcance (disponibilidad de datos). Está aclarado en el 03, el 04 y la conclusión del 05 | — | — |
| H6 | **Analizado y no reportado en el 05**: San Vicente, los CIIE, La Plata, la Región 23, los rankings de abandono municipal, la vista regional del abandono | Decisión (la conclusión del 05 los remite a los notebooks) | — | — |

**Columnas del padrón que no se analizaron** (qué aportarían):
- `area` (CONURBANO / INTERIOR): **útil**. Permite la comparación conurbano–interior (hallazgo nuevo 4).
- `desfavorabilidad` (0–5): índice de ruralidad o aislamiento. Está casi todo en estatales y rurales, y acompaña ofertas chicas; no se asocia con el abandono. Agrega poco.
- `subvencion`: aporte estatal a privados (de 40 % a 100 %). Serviría para un análisis de financiamiento, fuera de alcance.
- `categoria` (Primera, Segunda, Tercera): escala administrativa ligada al tamaño. Redundante con la matrícula.
- `depend_func` (13 direcciones): casi equivalente a la modalidad. Redundante.
- `turnos`: los patrones son los esperables (vespertino y noche en secundaria, superior y FP). Bajo valor.
- `sede_axo_ext`, `cue`, `anexo`, `nro_escuela`: identificadores administrativos.
- `telefono`, `email`, `rpv`, `direccion`: de contacto. No van.

## 5. Hallazgos nuevos

| Hallazgo | Dataset | Fuerza | ¿Vale la pena? | Notebook sugerido | Prioridad |
|---|---|---|---|---|---|
| **Los cargos docentes crecieron +20,2 % (491.441 → 590.851) mientras la matrícula creció +1,78 %; los alumnos por cargo bajaron de 10,0 a 8,46**, con subas en 130 de 135 municipios | Serie 2015–2025 (`docentes`) | Sólido a nivel provincial, con salvedades: son cargos, no personas, y hay saltos atípicos (A15) | **Alto**: el sistema creció poco en alumnos pero mucho en cargos | 02 (ya calculado; falta llevarlo a `02_cifras_informe.csv`) y 05, hallazgo 2 | Alta |
| **La expansión fue sobre todo de nivel inicial**: unos 170 de 519 eventos son jardines (33 %), contra unos 114 de secundaria, 83 de formación profesional o laboral y 66 de primaria | Expansión (`tipo_organizacion`, agrupado por nivel) | Sólido (conteo). La agrupación por nivel es aproximada (por nombre del tipo) | **Alto**: dice *qué* se expandió, algo que el informe hoy no cuenta | 03 (agrupación y gráfico) y 05, hallazgo 4 | Alta |
| Las reaperturas son 55 % rurales dispersas; las creaciones, 81 % urbanas | Expansión (`ambito` × `tipo_antecedente`) | Sólido (58 y 313 casos) | Medio: explica de dónde sale el peso rural de la expansión | 03 y contexto del hallazgo 4 del 05 | Media |
| El conurbano concentra el 58,3 % de la matrícula y solo el 37 % de los eventos. Entre 2015 y 2025, sus municipios crecieron menos que los del interior (mediana −0,98 % contra +2,99 %; 24 contra 111 municipios) | Padrón (`area`), expansión y serie | Moderado: son medianas municipales; conviene confirmarlo con totales agregados por área | Medio: agrega una lectura territorial que hoy no está | 02 y 03 | Media |
| Los privados tienen más alumnos por sección que los estatales: primaria 25,6 contra 16,4; secundaria 28,6 contra 22,7; inicial 18,2 contra 15,8 | Padrón (`matricula` / `secciones` × `sector`) | Sólido (miles de ofertas, medianas) | Medio: contexto para la estructura del sistema | 01 | Media |
| La divergencia municipal también ocurre dentro de las regiones: en 16 de 25 regiones hay municipios que crecen y otros que caen (Región 19: de −4,0 % a +34,0 %) | Serie 2015–2025 | Sólido | Medio: contexto del hallazgo 3 | 02 | Baja |
| El peso privado varía por nivel: alrededor de un tercio de la matrícula de inicial, primaria y secundaria; 17,5 % del superior; 5 % de la formación profesional | Padrón | Sólido | Medio: contexto del hallazgo 1 | 01 | Baja |
| Trayectorias de abandono no monótonas: 33 municipios bajaron y volvieron a subir más de 1 pp, y 15 subieron de forma sostenida | Abandono | Moderado: son municipios chicos y volátiles | Medio | 04 | Baja |
| La caída de 2020-21 no fue pareja: 69 municipios quedaron en 0,5 % o menos y 39 en negativo, pero 9 superaron el 3 % | Abandono | Sólido (descriptivo) | Medio | 04 | Baja |
| La desfavorabilidad está concentrada en ofertas rurales y chicas (mediana de 163 alumnos con índice 0, contra 5–7 con índice 3 a 5) | Padrón | Sólido pero esperable (es un índice de aislamiento) | Bajo | No va | Baja |
| Desfavorabilidad y abandono por municipio: Spearman 0,04 (135 municipios) | Padrón y abandono | Sin asociación | Bajo (descartado) | No va | Baja |
| Abandono conurbano contra interior: 2,92 % contra 2,80 % (mediana reciente) | Padrón y abandono | No hay brecha | Bajo (descartado; a lo sumo, una línea) | No va | Baja |
| Establecimientos en 2026 contra crecimiento 2015–2025: Spearman −0,27 (135) | Padrón y serie | Débil y probablemente espurio: lo explica que los municipios grandes del conurbano tienen muchas escuelas y crecieron menos | Bajo (descartado) | No va | Baja |
| Las reaperturas salen más por informe de la Secretaría de Inspección (14 de 58); el resto de los actos, casi todos por resolución | Expansión (`tipo_documento`) | Sólido, pero administrativo | Bajo | No va | Baja |
| Establecimientos con más de un evento: solo el 102873, que ya está documentado | Expansión | Confirmado | Bajo | No va | Baja |
| Subvención y tamaño: los privados con 70–80 % de subvención tienen ofertas más grandes (mediana 222–243 alumnos, contra 130 sin subvención) | Padrón | Sólido, pero lateral | Bajo | No va | Baja |
| Patrón conjunto expansión × matrícula × abandono | Cruces | No se exploró a fondo: con asociaciones de a pares débiles o nulas (0,36, 0,09, ≈0), es poco probable un patrón conjunto fuerte | Candidato para explorar después | — | Baja |

**Cierre**: de los 17 hallazgos encontrados, 2 son de prioridad alta, 3 de prioridad media y 12 de prioridad baja. Los de prioridad alta **no invierten** la narrativa del informe, pero la **completarían**: el de cargos docentes agrega una dimensión que matiza "el sistema creció poco" (creció poco en alumnos, mucho en cargos), y el de nivel inicial dice qué se expandió. Los de prioridad baja se descartan, salvo que quieras sumar alguno como una línea de contexto.

## 6. Huérfanos

| Archivo | Situación | Recomendación |
|---|---|---|
| `notebooks/evolucion_interactiva.html` (4,8 MB) | No lo genera ningún notebook ni lo referencia nadie; es anterior a esta revisión | Borrarlo, o moverlo a `backup/` si tiene valor histórico |
| 76 archivos de `outputs/` que el 05 no lee, sin contar los de control (28 del 01, 18 del 02, 15 del 03, 15 del 04) | Los generan los notebooks, salen en sus gráficos y tablas y están documentados (tablas completas, verificaciones, controles, cruces) | **Dejarlos** como auditables. No son basura: son la evidencia detrás de los textos de 01–04 |
| `outputs/0X_control_citas.csv` (5) | Los genera la celda de control de cada notebook | Dejarlos: son la prueba de que los textos cierran |
| `data/raw/establecimientos_educativos.csv` (truncado) | Lo usa solo la comparación del 01 | Dejarlo (referencia histórica pedida) |
| `backup/originales/` (2 notebooks) | Copia sin procesar de los notebooks anteriores a la revisión | Dejarlo |
| `establecimientos-educativos-metadatos.pdf` (raíz) | Metadatos de la fuente; ningún notebook lo usa | Dejarlo (documentación de la fuente) o moverlo a `data/raw/` |

## 7. Recomendación final

**Todavía no se puede publicar.** Antes hay que:
1. **C1 (bloqueante)**: completar `informe_config.json` y volver a generar el HTML con `src/publicar_informe.py`.
2. **C2 y C3**: corregir las dos frases del notebook 02 que contradicen los datos (son cambios de una línea; el 02 tiene que seguir dando 183/183 OK).
3. **Muy recomendable antes del push**: agregar `.gitignore` (A8) y la etiqueta `viewport` (A1). Son cambios chicos y evitan un repo inflado y un informe ilegible en el celular.

Después, a tu criterio: las advertencias A3–A7 y A9–A15, y los dos hallazgos de prioridad alta (cargos docentes y nivel inicial), que completarían el informe sin cambiar su estructura.
