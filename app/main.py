#main.py
from fastapi import FastAPI
from .routers import scrapping

app = FastAPI()

# Inclure les routeurs des différents endpoints
app.include_router(scrapping.router)

@app.get("/")
async def root():
    return {"message": "Bienvenue dans l'API de scrapping de données Wikipedia sur les émissions de CO2 par pays."}

