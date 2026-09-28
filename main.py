import os

from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from routes import router


app = FastAPI(
    title="ComicCraft",
    description="AI Comic Story Creator"
)


# --------------------------------
# Directories
# --------------------------------

os.makedirs(
    "static/generated",
    exist_ok=True
)


# --------------------------------
# Templates
# --------------------------------

templates = Jinja2Templates(
    directory="templates"
)


# --------------------------------
# Static files
# --------------------------------

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


# --------------------------------
# Routes
# --------------------------------

app.include_router(router)


@app.get("/")
def home(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )
@app.get("/export-success")
def export_success(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="export_success.html",
        context={}
    )
