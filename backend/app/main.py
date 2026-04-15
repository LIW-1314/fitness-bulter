from fastapi import FastAPI
from app.routes import bodyfat
from app.routes import diet
from app.routes import training
from app.routes import advice
from app.routes import chat
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()


@app.get("/")
def read_root():
    return {"message": "Fitness Butler API is running"}


@app.get("/ping")
def ping():
    return {"status": "ok"}


app.include_router(bodyfat.router, prefix="/bodyfat", tags=["bodyfat"])
app.include_router(diet.router, prefix="/diet", tags=["diet"])
app.include_router(training.router, prefix="/training", tags=["training"])
app.include_router(advice.router, prefix="/advice", tags=["advice"])
app.include_router(chat.router, prefix="/ai", tags=["ai"])