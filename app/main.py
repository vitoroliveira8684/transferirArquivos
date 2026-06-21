from fastapi import FastAPI;
from fastapi.staticfiles import StaticFiles;
from app.routes import files, auth;
from app.services.upload_service import create_table;

import os;

os.makedirs("uploads", exist_ok=True);

app = FastAPI();
create_table();

app.include_router(files.router);
app.include_router(auth.router);

app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.mount("/uploads", StaticFiles(directory="uploads"), name ="uploads")




