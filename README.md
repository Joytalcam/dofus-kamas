# 💰 Dofus Kamas Historical Rates

Scraper automatizado de la cotización del Kamas en la **Bolsa de Kamas de Dofus** (servidor Ogrinas), con visualización interactiva y publicación de datos abiertos.

## 📖 Descripción

Este proyecto extrae periódicamente la tasa de cambio del Kamas desde la página oficial de Dofus, almacena el histórico en un archivo CSV versionado en GitHub y lo publica en dos formatos:

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
```

🚀 Instalación y Uso Local
Si quieres replicar el proyecto en tu máquina:

Clona el repositorio:

bash
git clone https://github.com/Joytalcam/dofus-kamas.git
cd dofus-kamas
Crea un entorno virtual e instala las dependencias:

bash
python -m venv venv
# En Windows:
venv\Scripts\activate
# En Linux/Mac:
# source venv/bin/activate
pip install -r requirements.txt
Ejecuta el scraper para poblar los datos:

bash
python scraper.py
Lanza la app de visualización:

bash
streamlit run app.py
📊 Datos
Fuente: Bolsa de Kamas de Dofus

Variables:

Fecha: timestamp en UTC del momento de la cotización.

Tasa: precio del Kamas en la moneda del juego.

Frecuencia de actualización: cada 5 días (automático).

Limitaciones: Los datos son un "snapshot" del momento del scraping. Pueden existir huecos si la web no está disponible o si el WAF bloquea la petición.

🔗 Enlaces
App Streamlit: https://dofus-kamas.streamlit.app/

Dataset en Kaggle: https://www.kaggle.com/datasets/joytalcam/dofus-3-kamas-new-historical-rates

GitHub Actions: https://github.com/Joytalcam/dofus-kamas/actions

Repositorio GitHub: https://github.com/Joytalcam/dofus-kamas

🛠️ Tecnologías
Herramienta	Uso
Python 3.12	Lenguaje principal
Requests	Peticiones HTTP
BeautifulSoup4	Parseo de HTML
wafsolver	Bypass de AWS WAF
Pandas	Manipulación de datos
Streamlit	App de visualización
GitHub Actions	Automatización (CI/CD)
Kaggle API	Publicación del dataset
📄 Licencia
Código: MIT License.

Datos: CC0 1.0 Universal (dominio público).

🙏 Agradecimientos
A la comunidad de Dofus por mantener vivo el interés en la economía del juego.

A los mantenedores de wafsolver por facilitar el acceso a datos públicos.

A Streamlit y Kaggle por sus planes gratuitos que hacen posible este proyecto.

Última actualización: Noviembre 2026

text

### 📝 Cómo aplicarlo en GitHub

1. Ve a tu archivo `README.md` en GitHub.
2. Haz clic en el ícono del **lápiz** (Edit).
3. Selecciona **todo** el contenido actual (`Ctrl+A`) y bórralo.
4. Pega el bloque de arriba (el completo).
5. Baja hasta el final y haz clic en **Commit changes**.

---

Con esto, el README se verá exactamente como debe: con los bloques de código bien formateados, las listas con viñetas y la tabla de tecnologías renderizada. Cuéntame cuando lo tengas y revisamos el resultado. 🚀
