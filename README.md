# NC Invoice Manager

Lokāli hostējams rēķinu un pavadzīmju pārvaldības rīks (FastAPI + SQLite + Tailwind + ReportLab).

## Funkcijas
- 3 rēķinu tipi:
  - **Parasts rēķins** (ar apmaksājamo summu un summu vārdiem)
  - **Avansa rēķins** (atzīmēts kā avansa, filtrējams sarakstā, ar summu vārdiem)
  - **Avansa gala rēķins** (papildus lauki: iepriekš samaksāts + avansa rēķina atsauce)
- **Klientu rekvizītu saglabāšana** un automātiska aizpilde rēķinos.
- **Rēķina piestādītāja profilu saglabāšana** un automātiska aizpilde rēķinos.
- **Rēķinu saraksta sadaļa** ar meklēšanu, šķirošanu un filtrēšanu.
- **Dark mode** un vizuāli uzlabots UI ar ikonām.
- **Pavadzīmes** bez summām:
  - izsniedzēja vārds
  - saņēmēja vārds/uzvārds
  - piegādes adrese
- Visi dati glabājas lokālā **SQLite** datubāzē.
- Rēķinus un pavadzīmes var lejupielādēt **PDF** formātā.

## Startēšana izstrādei (dev)
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Atver: http://localhost:8000

## Windows .zip build (palaid uz Windows)
Šī daļa atrisina prasību: **lejupielādēt `.zip` un palaist uz Windows datora**.

1. Atver repo uz Windows.
2. Palaid:
   ```bat
   scripts\build_windows_zip.bat
   ```
3. Gatavais arhīvs būs:
   ```
   dist\NCInvoiceManager-windows.zip
   ```
4. Uz mērķa datora:
   - atzipot folderi,
   - palaist `run.bat`,
   - atvērt `http://127.0.0.1:8000`.

Dati glabājas failā `nc_invoice_manager.db` tajā pašā mapē, kur `run.bat`.

## EXE veidošana (manuāli)
Ja gribi manuāli:
```bat
python -m pip install -r requirements.txt pyinstaller
python -m PyInstaller --noconfirm --clean --name NCInvoiceManager --add-data "app\templates;app\templates" --add-data "app\static;app\static" --collect-all reportlab --collect-all jinja2 --collect-all starlette packaging\windows_entry.py
```
