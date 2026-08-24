#cd backend
#python -m uvicorn main:app --reload

from fastapi import FastAPI
from database import engine, Base
import models

app = FastAPI(title="SicherPlan API")

@app.get("/")
def home():
    return {"status": "Backend do SicherPlan rodando"}


Base.metadata.create_all(bind=engine)