import pandas as pd
import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Dofus Kamas - Histórico",
    page_icon="💰",
    layout="wide",
)

st.title("💰 Evolución del precio del Kamas - Dofus")
st.markdown("Datos históricos de la **Bolsa de Kamas** de Dofus (servidor Ogrinas).")

CSV_PATH = Path(__file__).parent / "data" / "kamas.csv"

if not CSV_PATH.exists():
    st.error("No se encontró el archivo de datos. Ejecuta `scraper.py` primero.")
    st.stop()

df = pd.read_csv(CSV_PATH, parse_dates=["Fecha"])
df = df.sort_values("Fecha").reset_index(drop=True)

col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Última tasa", f"{df['Tasa'].iloc[-1]:,.2f} k")
with col2:
    st.metric("Tasa mínima", f"{df['Tasa'].min():,.2f} k")
with col3:
    st.metric("Tasa máxima", f"{df['Tasa'].max():,.2f} k")

st.subheader("Histórico de tasas")
st.line_chart(df.set_index("Fecha")["Tasa"], color="#00C49A")

with st.expander("Ver tabla de datos completa"):
    st.dataframe(
        df.sort_values("Fecha", ascending=False).style.format({"Tasa": "{:,.2f}"}),
        use_container_width=True,
    )

st.caption(f"Datos actualizados hasta: {df['Fecha'].max().strftime('%Y-%m-%d %H:%M:%S')} UTC")
