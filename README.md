# NC Invoice Manager

Lokāli hostējams rēķinu un pavadzīmju pārvaldības rīks (FastAPI + SQLite + Tailwind + ReportLab).

## ✅ Gala lietotājam (1 klikšķis)
Tev vajag failu: **`NCInvoiceManager-windows.zip`**.

Kad to iegūsti:
1. Izpako zip.
2. Palaid `NCInvoiceManager.exe` (vai `run.bat`).
3. Atveras CMD ar statusu.
4. Pārlūks atveras automātiski uz `http://127.0.0.1:8000`.
5. Dati glabājas `nc_invoice_manager.db` blakus EXE.

## Kur dabūt gatavo ZIP no GitHub (bez būvēšanas uz sava PC)
### Variants A — Releases (ieteicamais)
1. Atver repozitoriju GitHub.
2. Labajā pusē sadaļā **Releases** atver jaunāko release.
3. Pie **Assets** lejupielādē `NCInvoiceManager-windows.zip`.

### Variants B — Actions Artifacts
1. Atver cilni **Actions**.
2. Atver pēdējo workflow **Build Windows ZIP** ar zaļu statusu.
3. Lejupielādē artifact: **NCInvoiceManager-windows**.
4. Atzipotajā artifact būs `NCInvoiceManager-windows.zip`.

## Izstrādātājam
### Lokāls build uz Windows
## ✅ Tev kā lietotājam (bez programmēšanas)
Tu teici pareizi — tev **nav jābūvē nekas**.

Tavs reālais scenārijs ir šāds:
1. Lejupielādē gatavu `NCInvoiceManager-windows.zip`.
2. Izpako zip.
3. Palaid `NCInvoiceManager.exe` (vai `run.bat`).
4. Atveras CMD logs ar statusu.
5. Automātiski atveras pārlūks uz `http://127.0.0.1:8000`.
6. Strādā ar aplikāciju.
7. Nākamajā reizē atkal tikai viens klikšķis uz `NCInvoiceManager.exe`.

Dati vienmēr saglabājas failā `nc_invoice_manager.db` tajā pašā mapē pie EXE.

---

## Funkcijas
- 3 rēķinu tipi (parasts, avansa, avansa gala).
- Klientu un piestādītāja rekvizītu saglabāšana.
- PDF ģenerēšana rēķiniem un pavadzīmēm.
- Tumšs interfeiss ar augšējo izvēlni.

---

## Tehniskā sadaļa (tikai izstrādātājam)
Šī sadaļa nav paredzēta gala lietotājam.

### Build uz Windows
```bat
scripts\build_windows_zip.bat
```
Rezultāts:
- `dist\NCInvoiceManager-windows.zip`
- iekšā: `NCInvoiceManager.exe`, `run.bat`, `README-WINDOWS.txt`

### Dev palaišana
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
