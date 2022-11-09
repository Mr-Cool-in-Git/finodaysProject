from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from ..models.accounts import (
    Account, AccountCreate, AccountUpdate
)
from ..services.accounts import AccountService

router = APIRouter(prefix='/accounts')

@router.get('/client_accounts', response_model=List[Account])
def get_all(id_client: int, service: AccountService = Depends()):
    return service.get_all(client_id=id_client)

@router.post('/', response_model = Account)
def create_account(
    account_data: AccountCreate,
    service: AccountService = Depends(),
):
    return service.create(account_data)

@router.put('/{account_id}', response_model = Account)
def update_account(
    account_id: int,
    amount: float,
    service: AccountService = Depends()
):
    return service.update(account_id, amount)

@router.delete('/{account_id}')
def delete_account(
    account_id: int,
    service: AccountService = Depends()
):
    service.delete(account_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)