from fastapi import Depends, HTTPException, status

from ..database import Session, get_session
from .. import tables

class ClientService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def verify(self, login: str, password: str) -> tables.Client:
        client = (
            self.session
                .query(tables.Client)
                .filter_by(login=login, password=password)
                .first()
        )
        if not client:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return client.id