# Instrumentación geotécnica — Proyecto Ituango

Aplicación estática de análisis estadístico sobre el **inventario del proyecto**. El dashboard se preparó en noviembre de 2026; **la fecha de corte del inventario no está acreditada** en la fuente.

> **Aviso de divulgación:** Esta entrega contiene datos estadísticos agregados. Antes de subirla a un repositorio público, obtener autorización de la entidad titular para publicar las estadísticas, incluidos los estados operativos agregados. No contiene identificadores de instrumentos, coordenadas ni observaciones de mantenimiento. GitHub Pages es público y no ofrece autorización por usuario.

## Funciones

- Filtros por obra, frente, tipo y estado de instalación; indicadores dependientes y comparaciones por frente.
- Gráficos de estado de instalación, distribución por tipo y frente, estado operativo **solo agregado por obra**, y año de instalación del inventario completo.
- Tabla paginada con búsqueda y exportación CSV.
- Mapa Leaflet; sin polígonos hasta recibir cartografía validada/autorizada, por lo que no contiene puntos o polígonos inventados.
- Tema claro/oscuro y visualización móvil.

**Unidad:** registro de la hoja `Listado` (8.042), no instrumento físico único. Se detectaron IDs repetidos con sensores/posiciones; por ello no se habilitó conteo deduplicado sin definir antes una clave de instrumento inequívoca. El agrupamiento de categorías pequeñas evita mostrar microcombinaciones frontales y no afecta el total de registros.

## Ver localmente

Requiere Python 3 para un servidor HTTP local (sin dependencias JavaScript):

```bash
python -m http.server 8000
```

Desde el directorio del proyecto, abrir `http://localhost:8000/`.

Los mapas base usan OpenStreetMap y Leaflet CDN, por lo que necesitan internet. La tabla y los indicadores se alimentan de `public/data/resumen_publico.json`.

## Actualizar datos **fuera del repositorio público**

1. Guardar el Excel en una carpeta local **fuera de Git**, por ejemplo `privado/LIST-INSTRUMENTOS_REV_25_EPM(1).xlsx`.
2. Instalar dependencia de preprocesamiento local `python -m pip install openpyxl`.
3. Ejecutar `python scripts/preparar_datos.py "privado/LIST-INSTRUMENTOS_REV_25_EPM(1).xlsx"`.
4. Revisar `scripts/reporte_validacion.json` (no subir si contiene detalles que no estén autorizados).
5. Inspeccionar el JSON generado en `public/data/resumen_publico.json`, aprobar institucionalmente y ejecutar `python scripts/verificar_publicacion.py`.

**Nunca subir el Excel original ni scripts con rutas privadas persistentes.** La transformación se ejecuta localmente y GitHub Actions solo publica el JSON ya autorizado. La autorización no puede automatizarse con una comprobación técnica.

## Geometrías de obras

Archivos vacíos `public/data/{presa,vertedero,subestacion,casa_maquinas,captacion,obras_descarga,tuneles_galerias,obras_principales,frentes}.geojson`.

Se pueden rellenar con cartografía GeoJSON en WGS84 solamente si sus geometrías y licencias fueron validadas y autorizadas. Cada feature puede tener propiedades `nombre` y opcionalmente `frente` para asociar una selección. No inferir polígonos a partir de los puntos del Excel. El estado actual es **sin geometrías publicables**.

## Publicar en GitHub Pages

1. Crear repositorio **nuevo** para este proyecto. No mezclar con `dashboard` de inundaciones.
2. Subir todo el contenido de esta carpeta **a la raíz** del repositorio.
3. Settings → Pages → Build and deployment → Source → **GitHub Actions**.
4. Revisar Actions → `Publicar observatorio Ituango` y su resultado.
5. Visitar `https://USUARIO.github.io/NOMBRE-REPOSITORIO/`.

Se utiliza HTML/CSS/JavaScript estático en vez de React/Vite para simplificar el despliegue y evitar compilación y dependencias JavaScript. Es un **cambio de implementación** respecto de la preferencia tecnológica del prompt; los gráficos son componentes dinámicos de HTML y CSS, no ECharts. El mapa usa Leaflet.

## Limitaciones y tareas pendientes

- **Sin geometrías verificadas de presa, vertedero, subestación u obras principales.** Son archivos GeoJSON válidos pero vacíos.
- Se necesita revisión institucional antes de publicar estadísticas relativas a infraestructura crítica.
- La vista agregada por obra de operatividad no debe confundirse con telemetría en tiempo real.
- No se permite cruzar estado operativo con frente/tipo en una página pública.
- El filtro por subfrente no está habilitado en la versión pública por el riesgo de microdesagregación.
- No se proporciona vista individual ni módulo interno autenticado.
- La fecha de corte del inventario no está verificada.
- No se prueba la URL de GitHub hasta su despliegue real.
