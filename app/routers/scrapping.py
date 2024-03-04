# app/routers/scrapping.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud
from ..dependencies import get_db

router = APIRouter()

@router.post("/scrape_and_save_in_database")
def wikipedia_scrapping(db: Session = Depends(get_db)):
    result = crud.scrape_and_save(db)
    if result == "Données déjà scrappées":
        raise HTTPException(status_code=400, detail=result)
    return {"message": "Scrapping réussi et données sauvegardées."}

