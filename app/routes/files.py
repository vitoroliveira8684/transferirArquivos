from fastapi import APIRouter, UploadFile, File, Request;
from fastapi.responses import HTMLResponse, RedirectResponse;
from fastapi.templating import Jinja2Templates;

import os;
import shutil;

router = APIRouter();


templates = Jinja2Templates(directory="app/templates");

@router.post("/upload")
def file_upload(file: UploadFile = File(...)):

    path = f"uploads/{file.filename}";

    with open(path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer);

    return RedirectResponse(url="/", status_code=303);


@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    files = os.listdir("uploads");

    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "request":request,
            "arquivos": files
        }
    )

@router.get("/uploads")
def ultimos():
    return os.listdir("uploads")

@router.post("/delete/{arquivo}")
def file_delete(arquivo: str):
    # prevent path traversal by using only the basename
    safe_name = os.path.basename(arquivo)
    path = os.path.join("uploads/", safe_name)

    if os.path.exists(path):
        os.remove(path)

    return RedirectResponse(url="/", status_code=303)

    

