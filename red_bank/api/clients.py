from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status

from ..models.clients import (
    Client
)
from ..services.clients import ClientService

router = APIRouter(
    prefix='/clients',
)

@router.get('/auth', response_model=int)
def verify_login(
        login: str,
        password: str,
        service: ClientService = Depends(),
):
    return service.verify(login=login, password=password)