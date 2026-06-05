from fastapi import FastAPI;
from fastapi.staticfiles import StaticFiles;
from app.routes import files;



app = FastAPI();

app.include_router(files.router);

app.mount("/uploads", StaticFiles(directory="uploads"), name ="uploads")




