from sqlalchemy.orm import Session
from . import models
import requests
from bs4 import BeautifulSoup

def scrape_and_save(db: Session):
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
