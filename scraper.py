import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import pandas as pd
import requests
import wafsolver
from bs4 import BeautifulSoup


URL = "https://www.dofus.com/es/compra-kamas/cotizacion-kama-ogrinas"
CSV_PATH = Path(__file__).parent / "data" / "kamas.csv"
DEBUG_PATH = Path(__file__).parent / "debug.html"
HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
}


def fetch_rates():
    domain = urlparse(URL).netloc
    session = requests.Session()
    session.headers.update(HEADERS)

    for intento in range(3):
        print(f"Intento {intento + 1}...")
        res = session.get(URL, timeout=30)

        # Comprobar si AWS WAF nos está desafiando
        if wafsolver.is_challenged(res.headers):
            print("  Desafío de AWS WAF detectado. Resolviendo...")
            try:
                token = wafsolver.solve_challenge(domain, res.text)
                # Guardar el token como cookie en la sesión
                session.cookies.set(wafsolver.TOKEN_COOKIE, token, domain=domain)
                print("  Token obtenido. Reintentando petición...")
                res = session.get(URL, timeout=30)
            except Exception as e:
                print(f"  Error resolviendo el desafío: {e}")

        soup = BeautifulSoup(res.text, "html.parser")

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

        # Si no encontramos RATES, guardamos el HTML para depurar
        print(f"  No se encontró RATES. Guardando HTML en debug.html")
        DEBUG_PATH.write_text(res.text, encoding="utf-8")
        time.sleep(5)

    raise RuntimeError("No se encontro la variable RATES tras 3 intentos. Revisa debug.html.")


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