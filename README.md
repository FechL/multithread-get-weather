# Komputasi Paralel Project

Program ini mengambil data cuaca dari beberapa kecamatan di **Papua Barat** secara **multithread** menggunakan API dari [WeatherAPI](https://www.weatherapi.com/).  
Hasilnya disimpan ke file Excel.

## Cara Menjalankan
1. Instal dependensi:
   ```bash
   pip install pandas requests python-dotenv openpyxl
   ````
2. Buat file `.env`:
   ```bash
   API_KEY=<masukkan_api_key_anda>
   ```
3. Pastikan file `papua_barat.xlsx` berisi daftar kecamatan.
4. Jalankan:

   ```bash
   python main.py
   ```

## Catatan
* Simpan `.env` di direktori yang sama dengan `main.py`.
* Jangan upload `.env` ke GitHub.

