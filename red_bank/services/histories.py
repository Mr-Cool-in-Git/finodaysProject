from fastapi import Depends
from typing import List

from ..database import Session, get_session
from ..models.histories import HistoryCreate
from .. import tables

class HistoryService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_all(self, client_id: int) -> List[tables.History]:
        query = self.session.query(tables.History)
        if client_id:
            query = query.filter_by(id_client=client_id)
        history = query.all()
        return history

    def create(self, history_data: HistoryCreate) -> tables.History:
        history = tables.History(**history_data.dict())
        self.session.add(history)
        self.session.commit()
        return history
