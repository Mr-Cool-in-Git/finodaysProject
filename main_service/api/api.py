from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

import fastapi
import plotly
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.graph_objs import Scatter
import requests

import pandas as pd
import numpy as np
import os
import json
from datetime import datetime

from fastapi import Form
from jinja2 import Template, Environment, FileSystemLoader
from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel

from ..services.users import UserService

BANK_MAPPING = {
    'green': 'Зеленый банк',
    'yellow': 'Желтый банк',
    'red': 'Красный банк'
}

router = APIRouter()
templates = Jinja2Templates(directory="main_service/templates")


@router.get('/', tags=["root"])
def get_all(request: Request):
    return templates.TemplateResponse("auth.html", {"request": request})


@router.post("/user/login", tags=["user"])
async def enter_user(login: str = Form(),
                     password: str = Form(), service: UserService = Depends()):
    id = service.get_token(login, password)

    if id:
        return fastapi.responses.RedirectResponse(
            f'/main_page/{id}',
            status_code=status.HTTP_302_FOUND)
    else:
        return fastapi.responses.RedirectResponse(
            f'/',
            status_code=status.HTTP_302_FOUND)


@router.post("/user/signup", tags=["user"])
async def create_user(login: str = Form(), name: str = Form(), password: str = Form(), service: UserService = Depends()):
    id = service.auth_new_user(login, name, password)


    if id:
        return fastapi.responses.RedirectResponse(
            f'/main_page/{id}',
            status_code=status.HTTP_302_FOUND)
    else:
        return fastapi.responses.RedirectResponse(
            f'/',
            status_code=status.HTTP_302_FOUND)


@router.get("/main_page/{id}", tags=["page"])
async def get_posts(id: str, request: Request,
                    user_service: UserService = Depends()):

    accounts_dict = user_service.get_accounts(id)
    nickname = user_service.get_name(id)
    money_report = user_service.money_report(accounts_dict['green_bank_id'],
                                             accounts_dict['yellow_bank_id'],
                                             accounts_dict['red_bank_id'])

    return templates.TemplateResponse("main_page.html", {"request": request,
                                                         "nickname": nickname,
                                                         "token": id,
                                                         "total_items": money_report['total_items'],
                                                         "green_items": money_report['green_items'],
                                                         "yellow_items": money_report['yellow_items'],
                                                         "red_items": money_report['red_items'],
                                                         "detailed_items": money_report['detailed_items'],
                                                         "greens_detailed_items" : money_report['greens_detailed_items'],
                                                         "yellow_detailed_items" : money_report['yellow_detailed_items'],
                                                         "red_detailed_items" : money_report['red_detailed_items']})


@router.get("/bank_connector/{bank}/{token}", tags=["page"])
async def get_posts(bank: str, token: str, request: Request,
                    user_service: UserService = Depends()):

    bank_naming = BANK_MAPPING[bank]
    return templates.TemplateResponse("bank_connector.html", {"request": request,
                                                              "bank_naming": bank_naming,
                                                              "color": bank,
                                                              "token": token})


@router.post("/connect/{bank}/{token}", tags=["user"])
async def connect_bank(bank: str, token: str, login: str = Form(),
                     password: str = Form(), service: UserService = Depends()):

    response = service.connect_bank(token, bank, login, password)
    if response:
        return fastapi.responses.RedirectResponse(
            f'/main_page/{token}',
            status_code=status.HTTP_302_FOUND)
    else:
        return fastapi.responses.RedirectResponse(
            f'/bank_connector/{bank}/{token}',
            status_code=status.HTTP_302_FOUND)


@router.get('/transactions/{token}', tags=["bank"])
def transactions_page(token: str, request: Request, service: UserService = Depends()):

    accounts_dict = service.get_accounts(token)
    money_report = service.money_accounts(accounts_dict['green_bank_id'],
                                          accounts_dict['yellow_bank_id'],
                                          accounts_dict['red_bank_id'])

    money_report['bank'] = money_report['bank'].map(BANK_MAPPING)

    accounts = []
    for i in range(money_report.shape[0]):
        an_item = dict(bank=money_report.loc[i, 'bank'],
                       number=money_report.loc[i, 'number'],
                       type=money_report.loc[i, 'type'],
                       amount=money_report.loc[i, 'amount'],
                       id=i)
        accounts.append(an_item)

    return templates.TemplateResponse("transactions.html", {"request": request, "accounts": accounts, "token": token})


def create_plot(init_df):
    init_df['date'] = init_df['date'].apply(lambda x: pd.to_datetime(x))
    init_df = init_df.groupby(['bank', 'date'])['amount'].sum().reset_index().sort_values('date')

    green_df = init_df.query('bank=="green"')
    yellow_df = init_df.query('bank=="yellow"')
    red_df = init_df.query('bank=="red"')

    data = []

    #if init_df.shape[0] != 0:
    data.append(go.Scatter(
        x=np.arange(0, init_df.shape[0]),
        y=init_df['amount'],
    ))

    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON


@router.get('/analytics/{token}', tags=["bank"])
def analytics_page(token: str, request: Request, service: UserService = Depends()):

     accounts_dict = service.get_accounts(token)
     money_report = service.money_history(accounts_dict['green_bank_id'],
                                              accounts_dict['yellow_bank_id'],
                                              accounts_dict['red_bank_id'])

     # plot
     fig = create_plot(money_report)
     print(fig)
     return templates.TemplateResponse("analytics.html", {"request": request, "plot": fig, "token": token})
