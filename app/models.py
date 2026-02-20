import enum
from sqlalchemy import Column, Integer, String, Float, Date, Enum, ForeignKey, Text
from sqlalchemy.orm import relationship
from .database import Base


class InvoiceType(str, enum.Enum):
    regular = "regular"
    advance = "advance"
    advance_final = "advance_final"


class PartyType(str, enum.Enum):
    client = "client"
    issuer = "issuer"


class Party(Base):
    __tablename__ = "parties"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    reg_no = Column(String, nullable=True)
    vat_no = Column(String, nullable=True)
    legal_address = Column(String, nullable=True)
    bank_name = Column(String, nullable=True)
    bank_account = Column(String, nullable=True)
    email = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    party_type = Column(Enum(PartyType), nullable=False, index=True)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    invoice_type = Column(Enum(InvoiceType), nullable=False, default=InvoiceType.regular)
    issue_date = Column(Date, nullable=False)
    due_date = Column(Date, nullable=False)

    seller_name = Column(String, nullable=False)
    seller_details = Column(Text, nullable=True)
    client_name = Column(String, nullable=False)
    client_details = Column(Text, nullable=True)

    seller_party_id = Column(Integer, ForeignKey("parties.id"), nullable=True)
    client_party_id = Column(Integer, ForeignKey("parties.id"), nullable=True)

    previous_paid_amount = Column(Float, nullable=True)
    previous_advance_reference = Column(String, nullable=True)

    notes = Column(Text, nullable=True)

    items = relationship("InvoiceItem", back_populates="invoice", cascade="all, delete-orphan")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, index=True)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=False)
    description = Column(String, nullable=False)
    unit = Column(String, nullable=False, default="gab")
    quantity = Column(Float, nullable=False)
    unit_price = Column(Float, nullable=False)

    invoice = relationship("Invoice", back_populates="items")


class DeliveryNote(Base):
    __tablename__ = "delivery_notes"

    id = Column(Integer, primary_key=True, index=True)
    number = Column(String, unique=True, nullable=False)
    issue_date = Column(Date, nullable=False)
    issuer_name = Column(String, nullable=False)
    receiver_name = Column(String, nullable=False)
    delivery_address = Column(String, nullable=False)
    notes = Column(Text, nullable=True)

    items = relationship("DeliveryNoteItem", back_populates="delivery_note", cascade="all, delete-orphan")


class DeliveryNoteItem(Base):
    __tablename__ = "delivery_note_items"

    id = Column(Integer, primary_key=True, index=True)
    delivery_note_id = Column(Integer, ForeignKey("delivery_notes.id"), nullable=False)
    description = Column(String, nullable=False)
    quantity = Column(Float, nullable=False)
    unit = Column(String, nullable=False, default="gab")

    delivery_note = relationship("DeliveryNote", back_populates="items")
