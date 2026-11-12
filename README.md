# 💰 Dofus Kamas Historical Rates

Scraper automatizado de la cotización del Kamas en la **Bolsa de Kamas de Dofus** (servidor Ogrinas), con visualización interactiva y publicación de datos abiertos.

## 📖 Descripción

Este proyecto extrae diariamente la tasa de cambio del Kamas desde la página oficial de Dofus, almacena el histórico en un archivo CSV versionado en GitHub y lo publica en dos formatos:

- Una **app web interactiva** (Streamlit) para visualizar la evolución del precio.
- Un **dataset público** (Kaggle) para que otros analistas o investigadores puedan usarlo.

El objetivo es ofrecer un registro transparente y accesible de la economía del juego, útil para jugadores, analistas de datos y estudios sobre economías virtuales.

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
└── README.md                  # Este archivo
