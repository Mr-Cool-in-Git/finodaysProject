from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from .api import router
import os

app = FastAPI()
app.include_router(router)


