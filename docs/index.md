# 💰 Dofus Kamas Historical Rates

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://dofus-kamas.streamlit.app/)
[![Kaggle Dataset](https://img.shields.io/badge/Kaggle-Dataset-20BEFF?logo=kaggle&logoColor=white)](https://www.kaggle.com/datasets/joytalcam/dofus-3-kamas-new-historical-rates)
[![Read the Docs](https://img.shields.io/badge/Docs-Read%20the%20Docs-8CA1AF?logo=readthedocs&logoColor=white)](https://dofus-kamas.readthedocs.io/)
[![GitHub Actions](https://img.shields.io/badge/GitHub%20Actions-Workflow-2088FF?logo=github-actions&logoColor=white)](https://github.com/Joytalcam/dofus-kamas/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![License: CC0-1.0](https://img.shields.io/badge/Data%20License-CC0--1.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Scraper automatizado de la cotización del Kamas en la **Bolsa de Kamas de Dofus** (servidor Ogrinas), con visualización interactiva, publicación de datos abiertos y documentación técnica.

## 📖 Descripción

Este proyecto extrae periódicamente la tasa de cambio del Kamas desde la página oficial de Dofus. El histórico se almacena en un archivo CSV versionado en GitHub y se publica en tres formatos:

- **App web interactiva (Streamlit):** Para visualizar la evolución del precio de forma gráfica.
- **Dataset público (Kaggle):** Para que otros analistas o investigadores puedan descargar y usar los datos.
- **Documentación (Read the Docs):** Para que cualquiera pueda entender, replicar y contribuir al proyecto.

**Objetivo:** Ofrecer un registro transparente y accesible de la economía del juego, útil para jugadores, analistas de datos y estudios sobre economías virtuales.

## 🏗️ Arquitectura del Proyecto

El flujo es completamente automático y no requiere intervención manual:

1. **GitHub Actions** se dispara cada 5 días (días 1, 6, 11, 16, 21, 26 y 31 a las 00:00 UTC).
2. Ejecuta `scraper.py`, que extrae los datos de la web de Dofus (resolviendo el desafío de AWS WAF con `wafsolver`).
3. Actualiza `data/kamas.csv` y hace un commit automático al repositorio.
4. **Streamlit Cloud** detecta el nuevo commit y actualiza la app pública.
5. Se sube una nueva versión del dataset a **Kaggle** mediante su API.

## 📂 Estructura del Repositorio

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
├── README.md                  # Este archivo
└── docs/                      # Documentación (Read the Docs)
    ├── index.md
    ├── conf.py
    └── requirements.txt
```

## 🚀 Instalación y Uso Local

Si quieres replicar el proyecto en tu máquina:

1. Clona el repositorio:
   ```bash
   git clone https://github.com/Joytalcam/dofus-kamas.git
   cd dofus-kamas
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En Linux/Mac:
   # source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Ejecuta el scraper para poblar los datos:
   ```bash
   python scraper.py
   ```

4. Lanza la app de visualización:
   ```bash
   streamlit run app.py
   ```

## 📊 Datos

- **Fuente:** Bolsa de Kamas de Dofus
- **Variables:**
  - *Fecha:* timestamp en UTC del momento de la cotización.
  - *Tasa:* precio del Kamas en la moneda del juego.
- **Frecuencia de actualización:** cada 5 días (automático).
- **Limitaciones:** Los datos son un "snapshot" del momento del scraping. Pueden existir huecos si la web no está disponible o si el WAF bloquea la petición.

## 🔗 Enlaces

- **App Streamlit:** [https://dofus-kamas.streamlit.app/](https://dofus-kamas.streamlit.app/)
- **Dataset en Kaggle:** [Kaggle Dataset](https://www.kaggle.com/datasets/joytalcam/dofus-3-kamas-new-historical-rates)
- **Documentación (Read the Docs):** [https://dofus-kamas.readthedocs.io/](https://dofus-kamas.readthedocs.io/)
- **GitHub Actions:** [GitHub Actions Workflow](https://github.com/Joytalcam/dofus-kamas/actions)
- **Repositorio GitHub:** [GitHub Repo](https://github.com/Joytalcam/dofus-kamas)

## 🛠️ Tecnologías

| Herramienta | Uso |
| :--- | :--- |
| **Python 3.12** | Lenguaje principal |
| **Requests** | Peticiones HTTP |
| **BeautifulSoup4** | Parseo de HTML |
| **wafsolver** | Bypass de AWS WAF |
| **Pandas** | Manipulación de datos |
| **Streamlit** | App de visualización |
| **GitHub Actions** | Automatización (CI/CD) |
| **Kaggle API** | Publicación del dataset |
| **Sphinx + MyST** | Documentación con Read the Docs |

## 📄 Licencia

- **Código:** MIT License.
- **Datos:** CC0 1.0 Universal (dominio público).

## 🙏 Agradecimientos

- A la comunidad de Dofus por mantener vivo el interés en la economía del juego.
- A los mantenedores de `wafsolver` por facilitar el acceso a datos públicos.
- A Streamlit, Kaggle y Read the Docs por sus planes gratuitos que hacen posible este proyecto.

---
*Última actualización: Noviembre 2026*
