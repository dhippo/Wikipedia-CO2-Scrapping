# app/crud.py
from sqlalchemy.orm import Session
from sqlalchemy import func
from . import models
import requests
from bs4 import BeautifulSoup
import csv
from io import StringIO

def scrape_and_save(db: Session):
    if check_data_exists(db):
        return "Données déjà scrappées"

    # Scrapping Wikipedia
    url = 'https://fr.wikipedia.org/wiki/Gaz_%C3%A0_effet_de_serre'
    response = requests.get(url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', id='bodyContent').text
    start_index = content.find("Approche consommationt CO2/personne")
    end_index = content.find("Approche territoriale : les émissions sont attribuées au pays sur le territoire duquel elles se produisent.Approche consommation")

    if start_index == -1 or end_index == -1:
        return None

    data = content[start_index:end_index]
    lines = [line for line in data.split('\n') if line.strip() != '']
    structured_data = structure_raw_data(lines[1:])

    for row in structured_data:
        db_emission = models.Emission(
            country_name=row[0],
            territorial_approach=row[1],
            territorial_approach_by_inhabitant=row[2],
            consumption_approach=row[3]
        )
        db.add(db_emission)

    db.commit()

def structure_raw_data(lines2):
    structured_data = []
    for i in range(0, len(lines2), 5):
        country = lines2[i].replace('\xa0', ' ')
        # Nettoyez et convertissez les données numériques
        territorial_approach = clean_and_convert_to_float(lines2[i + 1])
        consumption_approach = clean_and_convert_to_float(lines2[i + 2])
        consumption_approach_by_person = clean_and_convert_to_float(lines2[i + 3])
        structured_data.append([country, territorial_approach, consumption_approach, consumption_approach_by_person])
    return structured_data

def clean_and_convert_to_float(data_str):
    cleaned_str = data_str.replace('\xa0', '').replace(' ', '').replace(',', '.')
    return float(cleaned_str)

def check_data_exists(db: Session):
    return db.query(models.Emission).count() > 20


def scrape_and_save_csv():
    try:
        print("Début du scrapping Wikipedia")
        url = 'https://fr.wikipedia.org/wiki/Gaz_%C3%A0_effet_de_serre'
        response = requests.get(url)
        if response.status_code != 200:
            print("Erreur: Impossible d'accéder à la page Wikipedia")
            return None, "Erreur de réponse HTTP"

        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', id='bodyContent').text
        start_index = content.find("Approche consommationt CO2/personne")
        end_index = content.find(
            "Approche territoriale : les émissions sont attribuées au pays sur le territoire duquel elles se produisent.Approche consommation")

        if start_index == -1 or end_index == -1:
            print("Erreur: Impossible de trouver les indices de début et de fin dans la page")
            return None, "Indices de début et de fin non trouvés"

        data = content[start_index:end_index]
        lines = [line for line in data.split('\n') if line.strip() != '']
        print(f"Nombre de lignes extraites: {len(lines)}")

        structured_data = structure_raw_data(lines[1:])
        print("Données structurées créées")

        output = StringIO()
        writer = csv.writer(output)
        writer.writerow(['Country Name', 'Territorial Approach', 'Territorial Approach by Inhabitant', 'Consumption Approach'])

        for row in structured_data:
            writer.writerow(row)
        print("Données écrites dans le CSV")

        output.seek(0)
        return output.getvalue(), None
    except Exception as e:
        print(f"Erreur lors du scrapping ou de la génération du CSV: {e}")
        return None, str(e)


def get_total_territorial_approach(db: Session):
    total = db.query(func.sum(models.Emission.territorial_approach)) \
              .filter(models.Emission.country_name != "Union européenne") \
              .filter(models.Emission.country_name != "Monde") \
              .scalar()
    return total