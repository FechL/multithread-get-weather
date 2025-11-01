# Komputasi Paralel D Project1: Multithread, Oleh Kelompok 2
import pandas as pd
import requests
import threading
import time
import os
from dotenv import load_dotenv  # untuk membaca .env

# --- Load environment variables ---
load_dotenv()
API_KEY = os.getenv("API_KEY")

BASE_URL = "https://api.weatherapi.com/v1/current.json"
EXCEL_PATH = "papua_barat.xlsx"

class CuacaThread(threading.Thread):
    def __init__(self, kecamatan, hasil):
        super().__init__()
        self.kecamatan, self.hasil = kecamatan, hasil

    def run(self):
        start = time.perf_counter()
        try:
            r = requests.get(BASE_URL, params={
                "key": API_KEY,
                "q": f"{self.kecamatan}, Papua Barat, Indonesia",
                "aqi": "no"
            }, timeout=8)
            data = r.json().get("current", {})
            self.hasil[self.kecamatan] = (
                data.get("last_updated", "-"),
                data.get("temp_c", "-"),
                data.get("humidity", "-"),
                data.get("condition", {}).get("text", "-"),
                data.get("wind_kph", "-"),
                data.get("wind_dir", "-"),
                data.get("uv", "-")
            )
            durasi = time.perf_counter() - start
            print(f"[{durasi:.2f}s] OK, {self.kecamatan}")
        except Exception as e:
            durasi = time.perf_counter() - start
            print(f"[{durasi:.2f}s] FAIL, {self.kecamatan}: {e}")
            self.hasil[self.kecamatan] = ("Not Found",) * 7

def ambil_data_cuaca():
    try:
        df = pd.read_excel(EXCEL_PATH)
        kolom = df.columns[0]
        kecamatan = df[kolom].dropna().tolist()
        print(f"[>] Baca data kecamatan dari '{EXCEL_PATH}'")
    except Exception as e:
        return print(f"[>] Gagal baca file: {e}")

    hasil = {}
    threads = [CuacaThread(k, hasil) for k in kecamatan]

    t0 = time.time()
    for t in threads: 
        t.start()
    for t in threads: 
        t.join()

    ok_count = sum(1 for v in hasil.values() if v[0] != "Not Found")
    print(f"[>] Berhasil {ok_count}/{len(kecamatan)} kecamatan, selesai dalam {time.time() - t0:.2f} detik")
    
    kolom_hasil = ["Last Update","Suhu (C)","Kelembapan (%)","Kondisi","Angin (km/h)","Arah Angin","UV Index"]
    final = pd.concat([
        pd.DataFrame({kolom: kecamatan}),
        pd.DataFrame([hasil[k] for k in kecamatan], columns=kolom_hasil)
    ], axis=1)

    try:
        final.to_excel(EXCEL_PATH, index=False)
        print(f"[>] Data ditulis ke '{EXCEL_PATH}'")
    except Exception as e:
        print(f"[>] Gagal simpan: {e}")

if __name__ == "__main__":
    if not API_KEY:
        print("[!] API_KEY tidak ditemukan di file .env")
    else:
        ambil_data_cuaca()
