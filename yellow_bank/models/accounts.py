from pydantic import BaseModel
from datetime import date
from typing import Optional
from enum import Enum
from decimal import Decimal

class AccountKind(str, Enum):
    Card = 'card'
    Deposit = 'deposit'
    Credit = 'credit'
    Invest = 'invest'

class AccountBase(BaseModel):
    number: str
    id_client: int
    type: AccountKind
    amount: int

class Account(AccountBase):
    id: int

    class Config:
        orm_mode = True

class AccountUpdate(AccountBase):
    pass

class AccountCreate(AccountBase):
    pass