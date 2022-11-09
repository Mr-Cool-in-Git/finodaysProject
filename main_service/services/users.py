from typing import List, Optional
from fastapi import Depends, HTTPException, status

from ..database import Session, get_session
from ..models.model import User
from .. import tables


class OperationsService:
    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def _get(self, operation_id: int) -> tables.Operation:
        operation = (
            self.session
                .query(tables.Operation)
                .filter_by(id=operation_id)
                .first()
        )
        if not operation:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        return operation

    def create(self, user_data: User):
        operation = tables.Operation(**user_data.dict())
        user_sql = tables.User()
        user_sql.login = user.login
        user_sql.password = user.password

        session.add(operation)
        session.commit()
        return operation

    def update(self, operation_id: int, operation_data: OperationUpdate) -> tables.Operation:
        operation = self._get(operation_id)
        for field, value in operation_data:
            setattr(operation, field, value)
        self.session.commit()
        return operation

    def delete(self, operation_id: int):
        operation = self._get(operation_id)
        self.session.delete(operation)
        self.session.commit()
