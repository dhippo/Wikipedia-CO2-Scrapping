from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud
from ..dependencies import get_db

router = APIRouter()

@router.post("/wikipediascrapping/")
def wikipedia_scrapping(db: Session = Depends(get_db)):
    try:
        crud.scrape_and_save(db)
        return {"message": "Scrapping réussi et données sauvegardées."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
