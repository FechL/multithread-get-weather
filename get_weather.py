# Komputasi Paralel D Project1: Multithread, Oleh Kelompok 2
import pandas as pd
import requests
import threading
import time
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.weatherapi.com/v1/current.json"

# Load configuration (locations, output file, options)
try:
    from configuration import LOCATIONS, LOCATION_SUFFIX, OUTPUT_CSV, USE_AQI
except Exception:
    # Fallback defaults if configuration.py not present
    LOCATIONS = []
    LOCATION_SUFFIX = "Indonesia"
    OUTPUT_CSV = "output.csv"
    USE_AQI = True


class CuacaThread(threading.Thread):
    def __init__(self, kecamatan, hasil):
        super().__init__()
        self.kecamatan, self.hasil = kecamatan, hasil

    def run(self):
        start = time.perf_counter()
        try:
            q = self.kecamatan
            if LOCATION_SUFFIX:
                q = f"{self.kecamatan}, {LOCATION_SUFFIX}"

            r = requests.get(BASE_URL, params={
                "key": API_KEY,
                "q": q,
                "aqi": "yes" if USE_AQI else "no"
            }, timeout=8)

            current = r.json().get("current", {})
            aq = current.get("air_quality", {}) if USE_AQI else {}

            self.hasil[self.kecamatan] = (
                current.get("last_updated", "-"),
                current.get("temp_c", "-"),
                current.get("humidity", "-"),
                current.get("condition", {}).get("text", "-"),
                current.get("wind_kph", "-"),
                current.get("wind_dir", "-"),
                current.get("uv", "-"),

                # --- Air Quality ---
                aq.get("pm2_5", "-"),
                aq.get("pm10", "-"),
                aq.get("co", "-"),
                aq.get("no2", "-"),
                aq.get("o3", "-"),
                aq.get("so2", "-"),
                aq.get("us-epa-index", "-"),
            )

            durasi = time.perf_counter() - start
            print(f"[{durasi:.2f}s] OK, {self.kecamatan}")

        except Exception as e:
            durasi = time.perf_counter() - start
            print(f"[{durasi:.2f}s] FAIL, {self.kecamatan}: {e}")
            self.hasil[self.kecamatan] = ("Not Found",) * 14


def ambil_data_cuaca():
    # Determine list of locations: prefer LOCATIONS from config; else read from input excel
    if LOCATIONS:
        kecamatan = LOCATIONS
        print(f"[>] Menggunakan daftar lokasi dari 'configuration.py' ({len(kecamatan)} lokasi)")
    else:
        print("[>] Daftar lokasi kosong: isi `LOCATIONS` di `configuration.py` dengan lokasi yang ingin diambil cuacanya.")
        return

    hasil = {}
    threads = [CuacaThread(k, hasil) for k in kecamatan]

    t0 = time.time()
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    ok_count = sum(1 for v in hasil.values() if v[0] != "Not Found")
    print(f"[>] Berhasil {ok_count}/{len(kecamatan)} lokasi, selesai dalam {time.time() - t0:.2f} detik")

    kolom_hasil = [
        "Last Update", "Suhu (C)", "Kelembapan (%)", "Kondisi",
        "Angin (km/h)", "Arah Angin", "UV Index",

        # --- Kolom Polusi ---
        "PM2.5", "PM10", "CO", "NO2", "O3", "SO2", "US EPA Index"
    ]

    final = pd.concat([
        pd.DataFrame({"Lokasi": kecamatan}),
        pd.DataFrame([hasil[k] for k in kecamatan], columns=kolom_hasil)
    ], axis=1)

    try:
        final.to_csv(OUTPUT_CSV, index=False)
        print(f"[>] Data ditulis ke '{OUTPUT_CSV}'")
    except Exception as e:
        print(f"[>] Gagal simpan: {e}")


if __name__ == "__main__":
    if not API_KEY:
        print("[!] API_KEY tidak ditemukan di file .env")
    else:
        ambil_data_cuaca()
