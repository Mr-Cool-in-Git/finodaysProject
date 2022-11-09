from typing import List, Optional
from fastapi import APIRouter, Depends, Response, status
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

import fastapi

import os
import json

from jinja2 import Template, Environment, FileSystemLoader

from ..models.budgets import (
    Budget
)
from ..services.budgets import BudgetService

from fastapi import FastAPI, Body, Depends
from pydantic import BaseModel

from ..models import model
from ..models.model import UserSchema, UserLoginSchema
from ..auth.auth_bearer import JWTBearer
from ..auth.auth_handler import signJWT

posts = [
    {
        "id": 1,
        "title": "Pancake",
        "content": "Lorem Ipsum ..."
    }
]

from ..services.budgets import BudgetService

users = []

router = APIRouter()
templates = Jinja2Templates(directory="main_service/templates")

@router.get('/', tags=["root"])
def get_all(request: Request):
    return templates.TemplateResponse("empty_block.html", {"request": request})


@router.get("/main_page", dependencies=[Depends(JWTBearer())], tags=["page"])
async def get_posts(request: Request):
    return templates.TemplateResponse("main_page.html", {"request": request})
#
#
# @app.get("/posts/{id}", tags=["posts"])
# async def get_single_post(id: int) -> dict:
#     if id > len(posts):
#         return {
#             "error": "No such post with the supplied ID."
#         }
#
#     for post in posts:
#         if post["id"] == id:
#             return {
#                 "data": post
#             }
#
def check_user(data: UserLoginSchema):
    for user in users:
        if user.login == data.login and user.password == data.password:
            return True
    return False
#

class testUser(BaseModel):
    login: str = 'test'
    password: str = '0000'

from fastapi import Form

@router.post("/user/login", tags=["user"])
async def user_login(login: str = Form(),
                     password: str = Form()):
    user = UserLoginSchema(login=login, password=password)
    if check_user(user):
        return signJWT(user.login)
    return {
        "error": "Wrong login details!"
    }

# @app.post("/posts", dependencies=[Depends(JWTBearer())], tags=["posts"])
# async def add_post(post: PostSchema) -> dict:
#     post.id = len(posts) + 1
#     posts.append(post.dict())
#     return {
#         "data": "post added."
#     }

# LOGIN_URL = "https://example.com/login/oauth/authorize"
# REDIRECT_URL = f"{app}/auth/app"
# ...
# @router.get("/login")
# def get_login_url() -> model.Url:
#     return model.Url(url=f"{LOGIN_URL}?{urlencode(some_params_here)}")
#
# @router.post("/authorize")
# async def verify_authorization(body: model.AuthorizationResponse, db: Session = Depends(some_database_fetch)) -> Token:
#     return model.Token(access_token=access_token, token_type="bearer", user=User)
#
# def create_access_token(*, data: User, expire_time: int = None) -> bytes:
#     return encoded_jwt
# def get_user_from_header(*, authorization: str = Header(None)) -> User: # from fastapi import Header
#     return token_data   #Token data = User(**payload)
# @router.get("/me", response_model=User)
# def read_profile(user: User = Depends(get_user_from_header), db: Session = Depends(some_database_fetch),) -> DbUser:
#     return db_user

from .. import tables

@router.post("/user/signup", tags=["user"])
async def create_user(login: str = Form(),
                     password: str = Form()):
    user = UserLoginSchema(login=login, password=password)
    users.append(user)

    user_sql = tables.User()
    user_sql.login = user.login
    user_sql.password = user.password

    session.add(operation)
    session.commit()

    signJWT(user.login)

    return fastapi.responses.RedirectResponse(
        '/',
        headers={'Authorization': signJWT(user.login)['user_id']},
        status_code=status.HTTP_302_FOUND)

    #print(token)
    #unverified_header = jwt.get_unverified_header(token)

    #redirect_url = Request().url_for('get_posts', **{'Authorization': signJWT(user.login)})
    # return fastapi.responses.RedirectResponse(
    #     '/',
    #     headers={'Authorization': signJWT(user.login)['user_id']},
    #     status_code=status.HTTP_302_FOUND)

    return fastapi.responses.RedirectResponse(
            '/',
            status_code=status.HTTP_302_FOUND)
    #return signJWT(user.login)