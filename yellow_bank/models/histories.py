from pydantic import BaseModel
from datetime import date
from enum import Enum
from typing import Optional

class PaymentKind(str, Enum):
    Logistics = 'logistics'
    Shopping = 'shopping'
    Taxes = 'taxes'
    Subscriptions = 'subscriptions'
    Services = 'services'
    Transactions = 'transactions'
    Others = 'others'

class HistoryBase(BaseModel):
    id_client: int
    id_account: int
    date: date
    amount: float
    income: bool
    payment_kind: PaymentKind
    second_account: Optional[str]

class History(HistoryBase):
    id: int

    class Config:
        orm_mode = True

class HistoryCreate(HistoryBase):
    pass
