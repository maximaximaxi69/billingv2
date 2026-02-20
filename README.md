# NC Invoice Manager

Lokāli hostējams rēķinu un pavadzīmju pārvaldības rīks (FastAPI + SQLite + Tailwind + ReportLab).

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
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```
