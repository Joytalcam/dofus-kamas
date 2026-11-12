# 💰 Dofus Kamas Historical Rates

Bienvenido a la documentación oficial del proyecto **Dofus Kamas Historical Rates**.

Este proyecto automatiza la extracción, almacenamiento, visualización y publicación de la cotización del Kamas en la **Bolsa de Kamas de Dofus** (servidor Ogrinas).

---

## 📚 Índice de Contenidos

1. [📖 Descripción del Proyecto](#1--descripción-del-proyecto)
2. [🏗️ Arquitectura y Flujo de Trabajo](#2-️-arquitectura-y-flujo-de-trabajo)
3. [📂 Estructura del Repositorio](#3--estructura-del-repositorio)
4. [🚀 Guía de Instalación y Uso Local](#4--guía-de-instalación-y-uso-local)
5. [📊 Diccionario de Datos](#5--diccionario-de-datos)
6. [🔗 Enlaces y Recursos](#6--enlaces-y-recursos)
7. [🛠️ Tecnologías Utilizadas](#7-️-tecnologías-utilizadas)
8. [📄 Licencia y Agradecimientos](#8--licencia-y-agradecimientos)

---

## 1. 📖 Descripción del Proyecto

Este proyecto extrae periódicamente la tasa de cambio del Kamas desde la página oficial de Dofus. El histórico se almacena en un archivo CSV versionado en GitHub y se publica en dos formatos:

- **App web interactiva (Streamlit):** Para visualizar la evolución del precio de forma gráfica.
- **Dataset público (Kaggle):** Para que otros analistas o investigadores puedan descargar y usar los datos.

**Objetivo:** Ofrecer un registro transparente y accesible de la economía del juego, útil para jugadores, analistas de datos y estudios sobre economías virtuales.

---

## 2. 🏗️ Arquitectura y Flujo de Trabajo

El flujo es completamente automático y no requiere intervención manual:

1. **GitHub Actions** se dispara cada 5 días (días 1, 6, 11, 16, 21, 26 y 31 a las 00:00 UTC).
2. Ejecuta `scraper.py`, que extrae los datos de la web de Dofus (resolviendo el desafío de AWS WAF con `wafsolver`).
3. Actualiza `data/kamas.csv` y hace un commit automático al repositorio.
4. **Streamlit Cloud** detecta el nuevo commit y actualiza la app pública.
5. Se sube una nueva versión del dataset a **Kaggle** mediante su API.

---

## 3. 📂 Estructura del Repositorio

```text
.
├── data/
│   ├── kamas.csv              # Datos históricos (Fecha, Tasa)
│   └── dataset-metadata.json  # Metadatos para Kaggle
├── .github/workflows/
│   └── scraper.yml            # Workflow de automatización
├── scraper.py                 # Script de extracción
├── app.py                     # App de Streamlit
├── requirements.txt           # Dependencias del proyecto
├── README.md                  # Documentación principal
└── docs/                      # Esta documentación (Read the Docs)
    ├── index.md
    ├── conf.py
    └── requirements.txt
```

---

## 4. 🚀 Guía de Instalación y Uso Local

Si quieres replicar el proyecto en tu máquina:

### Paso 1: Clonar el repositorio

```bash
git clone https://github.com/Joytalcam/dofus-kamas.git
cd dofus-kamas
```

### Paso 2: Crear entorno virtual e instalar dependencias

```bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
# source venv/bin/activate
pip install -r requirements.txt
```

### Paso 3: Ejecutar el scraper

```bash
python scraper.py
```

### Paso 4: Lanzar la app de visualización

```bash
streamlit run app.py
```

---

## 5. 📊 Diccionario de Datos

| Variable | Tipo             | Descripción                              |
|----------|------------------|------------------------------------------|
| `Fecha`  | Timestamp (UTC)  | Momento exacto de la cotización.         |
| `Tasa`   | Float            | Precio del Kamas en la moneda del juego. |

- **Fuente:** [Bolsa de Kamas de Dofus](https://www.dofus.com/es/compra-kamas/cotizacion-kama-ogrinas)
- **Frecuencia de actualización:** Cada 5 días (automático).
- **Limitaciones:** Los datos son un "snapshot" del momento del scraping. Pueden existir huecos si la web no está disponible o si el WAF bloquea la petición.

---

## 6. 🔗 Enlaces y Recursos

- **App Streamlit:** <https://dofus-kamas.streamlit.app/>
- **Dataset en Kaggle:** <https://www.kaggle.com/datasets/joytalcam/dofus-3-kamas-new-historical-rates>
- **GitHub Actions:** <https://github.com/Joytalcam/dofus-kamas/actions>
- **Repositorio GitHub:** <https://github.com/Joytalcam/dofus-kamas>

---

## 7. 🛠️ Tecnologías Utilizadas

| Herramienta | Uso |
|-------------|-----|
| [Python 3.12](https://www.python.org/) | Lenguaje principal |
| [Requests](https://requests.readthedocs.io/) | Peticiones HTTP |
| [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) | Parseo de HTML |
| [wafsolver](https://pypi.org/project/wafsolver/) | Bypass de AWS WAF |
| [Pandas](https://pandas.pydata.org/) | Manipulación de datos |
| [Streamlit](https://streamlit.io/) | App de visualización |
| [GitHub Actions](https://github.com/features/actions) | Automatización (CI/CD) |
| [Kaggle API](https://github.com/Kaggle/kaggle-api) | Publicación del dataset |

---

## 8. 📄 Licencia y Agradecimientos

- **Código:** [MIT License](https://opensource.org/licenses/MIT).
- **Datos:** [CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/) (dominio público).

**Agradecimientos:**

- A la comunidad de Dofus por mantener vivo el interés en la economía del juego.
- A los mantenedores de `wafsolver` por facilitar el acceso a datos públicos.
- A [Streamlit](https://streamlit.io/) y [Kaggle](https://www.kaggle.com/) por sus planes gratuitos que hacen posible este proyecto.

---

*Última actualización: Noviembre 2026*
