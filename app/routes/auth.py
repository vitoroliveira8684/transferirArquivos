from fastapi import APIRouter, Request, Form, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

# Credenciais de teste (em produção, valide contra banco de dados)
USER_DATA = {"admin": "123456"}

@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request}
    )

@router.post("/login")
def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...)
):
    if USER_DATA.get(username) == password:
        response = RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
        # Salva o usuário no cookie HTTP-Only
        response.set_cookie(key="user_session", value=username, httponly=True)
        return response

    return templates.TemplateResponse(
        request=request,
        name="login.html",
        context={"request": request, "error": "Usuário ou senha incorretos"}
    )

@router.get("/logout")
def logout():
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("user_session")
    return response