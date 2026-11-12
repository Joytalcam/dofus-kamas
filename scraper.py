import json
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup


URL = "https://www.dofus.com/es/compra-kamas/cotizacion-kama-ogrinas"
CSV_PATH = Path(__file__).parent / "data" / "kamas.csv"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )
}


def fetch_rates():
    response = requests.get(URL, headers=HEADERS, timeout=30)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "html.parser")
    for script in soup.find_all("script"):
        if script.string and "RATES" in script.string:
            contenido = script.string
            idx = contenido.find("RATES = ")
            if idx == -1:
                continue
            inicio = idx + len("RATES = ")
            fin = contenido.find(";", inicio)
            if fin == -1:
                continue
            rates_json = contenido[inicio:fin].strip()
            return json.loads(rates_json)
    raise RuntimeError("No se encontro la variable RATES en el HTML.")


def parse_rates(rates_data):
    filas = []
    for ts, rate in rates_data.items():
        if ts == "avg" or rate is None:
            continue
        fecha = datetime.fromtimestamp(int(ts) / 1000, tz=timezone.utc)
        filas.append({"Fecha": fecha, "Tasa": float(rate)})
    df = pd.DataFrame(filas)
    if df.empty:
        return df
    return df.sort_values("Fecha").reset_index(drop=True)


def merge_with_existing(df_nuevos):
    if CSV_PATH.exists() and CSV_PATH.stat().st_size > 0:
        df_existente = pd.read_csv(CSV_PATH, parse_dates=["Fecha"])
    else:
        df_existente = pd.DataFrame(columns=["Fecha", "Tasa"])
    df_existente["Fecha"] = pd.to_datetime(df_existente["Fecha"], utc=True)
    df_existente["Tasa"] = pd.to_numeric(df_existente["Tasa"], errors="coerce")
    df_combined = pd.concat([df_existente, df_nuevos], ignore_index=True)
    df_combined = df_combined.drop_duplicates(subset=["Fecha"]).sort_values("Fecha")
    return df_combined.reset_index(drop=True)


def save_csv(df):
    CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    df_para_guardar = df.copy()
    df_para_guardar["Fecha"] = df_para_guardar["Fecha"].dt.strftime("%Y-%m-%d %H:%M:%S")
    df_para_guardar.to_csv(CSV_PATH, index=False, encoding="utf-8")


def main():
    print(f"[{datetime.now(timezone.utc).isoformat()}] Iniciando scraping...")
    try:
        rates_data = fetch_rates()
        print(f"  RATES obtenidos: {len(rates_data)} entradas.")
        df_nuevos = parse_rates(rates_data)
        print(f"  Filas validas: {len(df_nuevos)}")
        df_combined = merge_with_existing(df_nuevos)
        print(f"  Total filas tras merge: {len(df_combined)}")
        save_csv(df_combined)
        print(f"  Guardado en: {CSV_PATH}")
        return 0
    except Exception as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())