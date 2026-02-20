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
```bat
scripts\build_windows_zip.bat
```
Rezultāts:
- `dist\NCInvoiceManager-windows.zip`
- iekšā: `NCInvoiceManager.exe`, `run.bat`, `README-WINDOWS.txt`
