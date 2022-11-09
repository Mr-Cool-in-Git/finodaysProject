from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status

from ..models.histories import (
    History,
    HistoryCreate
)
from ..services.histories import HistoryService

router = APIRouter(
    prefix='/histories',
)

@router.get('/', response_model=List[History])
def get_operations(
        client_id: int,
        service: HistoryService = Depends(),
):
    return service.get_all(client_id=client_id)

@router.post('/', response_model = History)
def create(
    history_data: HistoryCreate,
    service: HistoryService = Depends(),
):
    return service.create(history_data)