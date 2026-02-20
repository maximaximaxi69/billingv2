from datetime import date
from typing import List, Optional
from pydantic import BaseModel, Field
from .models import InvoiceType, PartyType


class PartyCreate(BaseModel):
    name: str
    reg_no: Optional[str] = None
    vat_no: Optional[str] = None
    legal_address: Optional[str] = None
    bank_name: Optional[str] = None
    bank_account: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    party_type: PartyType


class InvoiceItemCreate(BaseModel):
    description: str
    unit: str = "gab"
    quantity: float = Field(gt=0)
    unit_price: float = Field(ge=0)


class InvoiceCreate(BaseModel):
    number: str
    invoice_type: InvoiceType
    issue_date: date
    due_date: date
    seller_name: str
    seller_details: Optional[str] = None
    client_name: str
    client_details: Optional[str] = None
    seller_party_id: Optional[int] = None
    client_party_id: Optional[int] = None
    previous_paid_amount: Optional[float] = Field(default=None, ge=0)
    previous_advance_reference: Optional[str] = None
    notes: Optional[str] = None
    items: List[InvoiceItemCreate]


class DeliveryNoteItemCreate(BaseModel):
    description: str
    quantity: float = Field(gt=0)
    unit: str = "gab"


class DeliveryNoteCreate(BaseModel):
    number: str
    issue_date: date
    issuer_name: str
    receiver_name: str
    delivery_address: str
    notes: Optional[str] = None
    items: List[DeliveryNoteItemCreate]
