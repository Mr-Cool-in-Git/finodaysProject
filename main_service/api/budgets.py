from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

import os
import json
import numpy as np

import plotly
import plotly.graph_objs as go
from plotly.offline import plot
from plotly.graph_objs import Scatter

from jinja2 import Template, Environment, FileSystemLoader

from ..models.budgets import (
    Budget
)
from ..services.budgets import BudgetService

router = APIRouter()
templates = Jinja2Templates(directory="main_service/templates")

def create_plot(init_df):
    data = [
        go.Scatter(
            x=np.array(range(0, init_df.shape[0])),
            y=init_df['amount'],
        )
    ]
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)
    return graphJSON

@router.get('/', response_model=List[Budget])
def get_all(request: Request):
    return templates.TemplateResponse("empty_block.html", {"request": request})

@router.get('/predict')
def get_all(
        service: BudgetService = Depends(),
):
    return service.predict()

@router.get("/budget_spb", response_class=HTMLResponse)
async def total_table(request: Request, service: BudgetService = Depends()):
    total_dict = service.total_table()

    # table
    items = []
    for i in total_dict['df'].values:
        an_item = dict(fact_1=i[0], fact_2=i[1], amount=i[2], is_predict=i[3])
        items.append(an_item)

    # plot
    fig = create_plot(total_dict['df'])
    return templates.TemplateResponse("main_page.html", {"request": request, "items": items, "plot": fig})