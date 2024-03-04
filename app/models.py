# app/models.py
from sqlalchemy import Column, Integer, Float, String
from .dependencies import Base

class Emission(Base):
    __tablename__ = "emissions_by_country"

    id = Column(Integer, primary_key=True, autoincrement=True)  # Clé primaire ajoutée
    country_name = Column(String(255), nullable=False)
    territorial_approach = Column(Float)
    territorial_approach_by_inhabitant = Column(Float)
    consumption_approach = Column(Float)

