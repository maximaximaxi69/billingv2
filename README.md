# NC Invoice Manager

Lokāli hostējams rēķinu un pavadzīmju pārvaldības rīks (FastAPI + SQLite + Tailwind + ReportLab).

## Funkcijas
- 3 rēķinu tipi (parasts, avansa, avansa gala).
- Klientu un piestādītāja rekvizītu saglabāšana.
- PDF ģenerēšana rēķiniem un pavadzīmēm.
- Tumšs interfeiss ar augšējo izvēlni līdzīgi pievienotajam paraugam.

## Kā strādā Windows `.zip`
Mērķa scenārijs:
1. Lejupielādē ZIP.
2. Izpako.
3. Palaiž EXE.
4. Atveras CMD logs ar statusu (ports, datu fails, servera gatavība).
5. Automātiski atveras Chrome (ja pieejams), citādi noklusētais pārlūks uz `http://127.0.0.1:8000`.

Tas ir realizēts ar `packaging/windows_entry.py` + build skriptiem.

## Build uz Windows
```bat
scripts\build_windows_zip.bat
```
Rezultāts:
- `dist\NCInvoiceManager-windows.zip`
- iekšā: `NCInvoiceManager.exe`, `run.bat`, `README-WINDOWS.txt`

## Dev palaišana
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
