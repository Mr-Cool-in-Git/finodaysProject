from fastapi import Depends, HTTPException, status
from typing import List, Optional

from ..database import Session, get_session
from ..models.accounts import AccountKind, AccountCreate, AccountUpdate
from .. import tables

class AccountService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, id: int) -> tables.Account:
        account = (
            self.session
                .query(tables.Account)
                .filter_by(id=id)
                .first()
        )
        if not account:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return account

    def get_all(self, client_id: int) -> List[tables.Account]:
        query = self.session.query(tables.Account)
        if client_id:
            query = query.filter_by(id_client=client_id)
        accounts = query.all()
        return accounts

    def update(self, account_id: int, amount: float) -> tables.Account:
        account = self._get(account_id)
        account.amount = amount
        # for field, value in account_data:
        #     print(field, value)
        #     setattr(account, field, value)
        self.session.commit()
        return account

    def create(self, account_data: AccountCreate) -> tables.Account:
        account = tables.Account(**account_data.dict())
        self.session.add(account)
        self.session.commit()
        return account

    def delete(self, account_id: int):
        account = self._get(account_id)
        self.session.delete(account)
        self.session.commit()