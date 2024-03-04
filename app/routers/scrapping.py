# app/routers/scrapping.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
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


@router.get("/scrape_and_save_csv")
def wikipedia_scrapping_csv():
    csv_data, error = crud.scrape_and_save_csv()

    if error:  # Si une erreur est renvoyée
        raise HTTPException(status_code=500, detail=f"Erreur importante lors du scrapping ou de la génération du CSV: {error}")

    # Création d'une réponse StreamingResponse pour renvoyer le fichier CSV
    response = StreamingResponse(iter([csv_data]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=emissions_data.csv"
    return response

@router.get("/SUM_total_territorial_approach")
def total_territorial_approach(db: Session = Depends(get_db)):
    total = crud.get_total_territorial_approach(db)
    return {"total_territorial_approach": total}

