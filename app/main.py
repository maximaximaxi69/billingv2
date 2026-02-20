from datetime import date
from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.responses import HTMLResponse, Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
from sqlalchemy import select, text

from .database import Base, engine, get_db
from .models import Invoice, InvoiceItem, DeliveryNote, DeliveryNoteItem, InvoiceType, Party, PartyType
from .schemas import InvoiceCreate, DeliveryNoteCreate, PartyCreate
from .pdf import generate_invoice_pdf, generate_delivery_note_pdf

app = FastAPI(title="NC Invoice Manager")
Base.metadata.create_all(bind=engine)


APP_DIR = Path(__file__).resolve().parent
STATIC_DIR = APP_DIR / "static"
TEMPLATES_DIR = APP_DIR / "templates"


def ensure_sqlite_migrations():
    with engine.begin() as conn:
        conn.execute(text("CREATE TABLE IF NOT EXISTS parties (id INTEGER PRIMARY KEY, name VARCHAR NOT NULL, reg_no VARCHAR, vat_no VARCHAR, legal_address VARCHAR, bank_name VARCHAR, bank_account VARCHAR, email VARCHAR, phone VARCHAR, party_type VARCHAR NOT NULL)"))
        columns = {row[1] for row in conn.execute(text("PRAGMA table_info(invoices)"))}
        if "seller_party_id" not in columns:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN seller_party_id INTEGER"))
        if "client_party_id" not in columns:
            conn.execute(text("ALTER TABLE invoices ADD COLUMN client_party_id INTEGER"))


ensure_sqlite_migrations()

app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/parties")
def create_party(payload: PartyCreate, db: Session = Depends(get_db)):
    entity = Party(**payload.model_dump())
    db.add(entity)
    db.commit()
    db.refresh(entity)
    return {"id": entity.id}


@app.get("/api/parties")
def list_parties(party_type: PartyType | None = None, db: Session = Depends(get_db)):
    stmt = select(Party)
    if party_type:
        stmt = stmt.where(Party.party_type == party_type)
    rows = db.scalars(stmt.order_by(Party.name.asc())).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "reg_no": p.reg_no,
            "vat_no": p.vat_no,
            "legal_address": p.legal_address,
            "bank_name": p.bank_name,
            "bank_account": p.bank_account,
            "email": p.email,
            "phone": p.phone,
            "party_type": p.party_type.value,
        }
        for p in rows
    ]


@app.post("/api/invoices")
def create_invoice(payload: InvoiceCreate, db: Session = Depends(get_db)):
    if payload.invoice_type == InvoiceType.advance_final and payload.previous_paid_amount is None:
        raise HTTPException(status_code=400, detail="Avansa gala rēķinam jānorāda iepriekš samaksātā summa.")

    invoice = Invoice(**payload.model_dump(exclude={"items"}))
    for item in payload.items:
        invoice.items.append(InvoiceItem(description=item.description, unit=item.unit, quantity=item.quantity, unit_price=item.unit_price))

    db.add(invoice)
    db.commit()
    db.refresh(invoice)
    return {"id": invoice.id}


@app.get("/api/invoices")
def list_invoices(
    invoice_type: InvoiceType | None = None,
    q: str | None = Query(default=None, description="Search by invoice no/client"),
    sort: str = Query(default="issue_date_desc"),
    db: Session = Depends(get_db),
):
    stmt = select(Invoice)
    if invoice_type:
        stmt = stmt.where(Invoice.invoice_type == invoice_type)
    if q:
        like = f"%{q.strip()}%"
        stmt = stmt.where((Invoice.number.like(like)) | (Invoice.client_name.like(like)))

    if sort == "issue_date_asc":
        stmt = stmt.order_by(Invoice.issue_date.asc(), Invoice.id.asc())
    elif sort == "amount_desc":
        stmt = stmt.order_by(Invoice.id.desc())
    elif sort == "amount_asc":
        stmt = stmt.order_by(Invoice.id.asc())
    else:
        stmt = stmt.order_by(Invoice.issue_date.desc(), Invoice.id.desc())

    rows = db.scalars(stmt).all()

    result = []
    for i in rows:
        total = sum(x.quantity * x.unit_price for x in i.items)
        payable = total - (i.previous_paid_amount or 0.0) if i.invoice_type == InvoiceType.advance_final else total
        result.append({
            "id": i.id,
            "number": i.number,
            "invoice_type": i.invoice_type.value,
            "issue_date": str(i.issue_date),
            "due_date": str(i.due_date),
            "client_name": i.client_name,
            "seller_name": i.seller_name,
            "total": round(total, 2),
            "payable": round(payable, 2),
        })

    if sort == "amount_desc":
        result.sort(key=lambda x: x["payable"], reverse=True)
    if sort == "amount_asc":
        result.sort(key=lambda x: x["payable"])

    return result


@app.get("/api/invoices/{invoice_id}/pdf")
def invoice_pdf(invoice_id: int, db: Session = Depends(get_db)):
    invoice = db.get(Invoice, invoice_id)
    if not invoice:
        raise HTTPException(status_code=404, detail="Rēķins nav atrasts")
    pdf = generate_invoice_pdf(invoice)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=invoice-{invoice.number}.pdf"})


@app.post("/api/delivery-notes")
def create_delivery_note(payload: DeliveryNoteCreate, db: Session = Depends(get_db)):
    note = DeliveryNote(
        number=payload.number,
        issue_date=payload.issue_date,
        issuer_name=payload.issuer_name,
        receiver_name=payload.receiver_name,
        delivery_address=payload.delivery_address,
        notes=payload.notes,
    )
    for item in payload.items:
        note.items.append(DeliveryNoteItem(description=item.description, quantity=item.quantity, unit=item.unit))

    db.add(note)
    db.commit()
    db.refresh(note)
    return {"id": note.id}


@app.get("/api/delivery-notes")
def list_delivery_notes(db: Session = Depends(get_db)):
    rows = db.scalars(select(DeliveryNote).order_by(DeliveryNote.id.desc())).all()
    return [{"id": n.id, "number": n.number, "issue_date": str(n.issue_date), "receiver_name": n.receiver_name} for n in rows]


@app.get("/api/delivery-notes/{note_id}/pdf")
def delivery_note_pdf(note_id: int, db: Session = Depends(get_db)):
    note = db.get(DeliveryNote, note_id)
    if not note:
        raise HTTPException(status_code=404, detail="Pavadzīme nav atrasta")
    pdf = generate_delivery_note_pdf(note)
    return Response(content=pdf, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=delivery-note-{note.number}.pdf"})


@app.get("/api/health")
def health():
    return {"ok": True, "date": str(date.today())}
