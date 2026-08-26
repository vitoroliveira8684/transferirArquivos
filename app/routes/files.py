from fastapi import APIRouter, UploadFile, File, Request, status;
from fastapi.responses import HTMLResponse, RedirectResponse;
from fastapi.templating import Jinja2Templates;

import os;
import shutil;

router = APIRouter();
templates = Jinja2Templates(directory="app/templates");

def get_current_user(request: Request):
    """
    Função auxiliar que lê os cookies do navegador e 
    retorna o nome do usuário se ele estiver logado
    """
    return request.cookies.get("user_session");




@router.get("/", response_class=HTMLResponse)
def home(request: Request):

    user = get_current_user(request);

    if not user:
        return RedirectResponse(
            url="/login", status_code=status.HTTP_303_SEE_OTHER
        )
    
    files = os.listdir("uploads");

    return templates.TemplateResponse(
        request = request,
        name = "index.html",
        context = {
            "request":request,
            "arquivos": files,
            "user": user,
        },
    )

@router.post("/upload")
def file_upload(request: Request, files: list[UploadFile] = File(...)):

    # proteção de autenticação
    if not get_current_user(request):
        return RedirectResponse(
            url="/login", status_code=status.HTTP_303_SEE_OTHER
        )
    for file in files:
        if not file.filename:
            continue
        path = f"uploads/{file.filename}";
        # salva cada arquivo no disco
        with open(path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer);

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER);



@router.get("/uploads")
def ultimos(request: Request):

    if not get_current_user(request):
        return RedirectResponse(
            url="/login", status_code=status.HTTP_303_SEE_OTHER
        )
    
    return os.listdir("uploads")

@router.post("/delete/{arquivo}")
def file_delete(request: Request, arquivo: str):
    
    if not get_current_user(request):
        return RedirectResponse(
            url="/login", status_code=status.HTTP_303_SEE_OTHER
        )

    # prevent path traversal by using only the basename
    safe_name = os.path.basename(arquivo)
    path = os.path.join("uploads/", safe_name)

    if os.path.exists(path):
        os.remove(path)

    return RedirectResponse(url="/", status_code=303)

    

