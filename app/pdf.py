from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from .amount_words_lv import number_to_words_lv
from .models import Invoice, InvoiceType, DeliveryNote


def _draw_header(c: canvas.Canvas, title: str, number: str, issue_date):
    c.setFont("Helvetica-Bold", 16)
    c.drawString(20 * mm, 280 * mm, title)
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, 273 * mm, f"Nr.: {number}")
    c.drawString(20 * mm, 267 * mm, f"Datums: {issue_date}")


def generate_invoice_pdf(invoice: Invoice) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    title_map = {
        InvoiceType.regular: "RĒĶINS",
        InvoiceType.advance: "AVANSA RĒĶINS",
        InvoiceType.advance_final: "AVANSA GALA RĒĶINS",
    }
    _draw_header(c, title_map[invoice.invoice_type], invoice.number, invoice.issue_date)

    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, 257 * mm, f"Pārdevējs: {invoice.seller_name}")
    c.drawString(20 * mm, 251 * mm, f"Pircējs: {invoice.client_name}")

    y = 235 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Apraksts")
    c.drawString(120 * mm, y, "Daudzums")
    c.drawString(145 * mm, y, "Cena")
    c.drawString(170 * mm, y, "Summa")

    c.setFont("Helvetica", 10)
    total = 0.0
    y -= 7 * mm
    for item in invoice.items:
        line_total = item.quantity * item.unit_price
        total += line_total
        c.drawString(20 * mm, y, item.description[:45])
        c.drawRightString(140 * mm, y, f"{item.quantity:.2f} {item.unit}")
        c.drawRightString(165 * mm, y, f"{item.unit_price:.2f}")
        c.drawRightString(195 * mm, y, f"{line_total:.2f}")
        y -= 6 * mm

    c.setFont("Helvetica-Bold", 11)
    c.drawRightString(195 * mm, y - 4 * mm, f"Kopā: {total:.2f} EUR")

    payable = total
    if invoice.invoice_type == InvoiceType.advance_final:
        prev = invoice.previous_paid_amount or 0.0
        c.setFont("Helvetica", 10)
        c.drawString(20 * mm, y - 12 * mm, f"Iepriekš samaksāts: {prev:.2f} EUR")
        if invoice.previous_advance_reference:
            c.drawString(20 * mm, y - 18 * mm, f"Saskaņā ar avansa rēķinu: {invoice.previous_advance_reference}")
        payable = total - prev

    c.setFont("Helvetica-Bold", 12)
    c.drawRightString(195 * mm, y - 26 * mm, f"Apmaksājamā summa: {payable:.2f} EUR")
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, y - 33 * mm, f"Summa vārdiem: {number_to_words_lv(max(payable, 0.0))}")

    if invoice.notes:
        c.drawString(20 * mm, y - 42 * mm, f"Piezīmes: {invoice.notes[:100]}")

    c.showPage()
    c.save()
    return buf.getvalue()


def generate_delivery_note_pdf(note: DeliveryNote) -> bytes:
    buf = BytesIO()
    c = canvas.Canvas(buf, pagesize=A4)

    _draw_header(c, "PAVADZĪME", note.number, note.issue_date)
    c.setFont("Helvetica", 10)
    c.drawString(20 * mm, 257 * mm, f"Izsniedzējs: {note.issuer_name}")
    c.drawString(20 * mm, 251 * mm, f"Saņēmējs: {note.receiver_name}")
    c.drawString(20 * mm, 245 * mm, f"Piegādes adrese: {note.delivery_address}")

    y = 230 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Apraksts")
    c.drawString(145 * mm, y, "Daudzums")
    c.drawString(180 * mm, y, "Mērv.")

    c.setFont("Helvetica", 10)
    y -= 7 * mm
    for item in note.items:
        c.drawString(20 * mm, y, item.description[:60])
        c.drawRightString(170 * mm, y, f"{item.quantity:.2f}")
        c.drawRightString(195 * mm, y, item.unit)
        y -= 6 * mm

    if note.notes:
        c.drawString(20 * mm, y - 8 * mm, f"Piezīmes: {note.notes[:100]}")

    c.showPage()
    c.save()
    return buf.getvalue()
