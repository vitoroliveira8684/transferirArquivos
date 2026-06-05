from fastapi import APIRouter, UploadFile, File, Request;
from fastapi.responses import HTMLResponse;
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

    return{
        "nome": file.filename,
        "status": "sucesso",
    }


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

    

