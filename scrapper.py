import requests
from bs4 import BeautifulSoup
import mysql.connector
import os

def scrapping_wikipedia_data():
    # Charger la page Wikipedia
    url = 'https://fr.wikipedia.org/wiki/Gaz_%C3%A0_effet_de_serre'
    response = requests.get(url)

    if response.status_code == 200:
        # Analyser la page avec BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', id='bodyContent').text

        # Trouver les données à extraire
        start_index = content.find("Approche consommationt CO2/personne")
        end_index = content.find("Approche territoriale : les émissions sont attribuées au pays sur le territoire duquel elles se produisent.Approche consommation")

        if start_index != -1 and end_index != -1:
            # Extraire les données
            data = content[start_index:end_index]

        else:
            print("Phrases clés non trouvées.")

        raw_data = data

        lines = [line for line in raw_data.split('\n') if line.strip() != '']

        lines2 = lines[1:]

        # Structurer les données brutes
        return structure_raw_data(lines2)
    else:
        print(f'Erreur récupération page: Code {response.status_code}')
        return []

def structure_raw_data(lines2):
    structured_data = []
    # Structurer chaque ligne
    for i in range(0, len(lines2), 5):
        country = lines2[i].replace('\xa0', ' ')
        territorial_approach = lines2[i + 1].replace('\xa0', ' ')
        consumption_approach = lines2[i + 2]
        consumption_approach_by_person = lines2[i + 3].replace('\xa0', ' ')
        # Ajouter données structurées
        structured_data.append([country, territorial_approach, consumption_approach, consumption_approach_by_person])
    return structured_data

def clean_and_structure_data(data_string):
    # Convertir et nettoyer les données
    data_converted = []
    for row in data_string:
        new_row = []
        for item in row:
            # Supprimer les espaces inutiles
            cleaned_item = item.replace(" ", "").strip()
            # Convertir en nombre si l'item est numérique
            if cleaned_item.replace(",", "").replace(".", "").isdigit():
                if ',' in cleaned_item or '.' in cleaned_item:
                    # Convertir en float si l'item a une virgule ou un point
                    new_item = float(cleaned_item.replace(",", "."))
                else:
                    # Convertir en int si l'item est un entier
                    new_item = int(cleaned_item)
            else:
                # Garder la chaîne telle quelle si elle n'est pas numérique
                new_item = item.strip()
            new_row.append(new_item)
        data_converted.append(new_row)
    print('data_converted')
    print(data_converted)
    #output : [['Chine', 10151, 7.3, 8392], ['États-Unis', 5411, 17, 5886], ['Union européenne', 3501, 6.9, 4315], ['Inde', 2320, 1.8, 2171], ['Russie', 1671, 12, 1338], ['Japon', 1225, 9.6, 1451], ['Allemagne', 792, 9.7, 902], ['Iran', 642, 8.1, 525], ['Corée du Sud', 592, 12, 662], ['Canada', 568, 16, 584], ['Arabie saoudite', 524, 16.6, 634], ['Brésil', 523, 2.5, 550], ['Mexique', 477, 3.8, 526], ['Indonésie', 469, 1.8, 484], ['Afrique du Sud', 462, 8.3, 371], ['Royaume-Uni', 416, 6.4, 596], ['Australie', 402, 17, 394], ['Turquie', 383, 4.9, 436], ['Italie', 357, 6.0, 480], ['France', 337, 5.2, 458], ['Thaïlande', 323, 4.7, 308], ['Pologne', 311, 8.1, 301], ['Espagne', 272, 5.9, 306], ['Taïwan', 262, 11, 271], ['Malaisie', 249, 8.1, 251], ['Kazakhstan', 230, 13, 213], ['Ukraine', 223, 5.0, 245], ['Argentine', 208, 4.8, 210], ['Égypte', 207, 2.2, 196], ['Monde', 36019, 4.9, 36019]]

    return data_converted



def enregistrer_en_bdd(structured_data):
    # affichage des variables d'environnement pour être sûr qu'elles soient récupérées (exécuter "docker run" avec le paramètre --env-file .env)
    print("DB_HOST:", os.getenv('DB_HOST'))
    print("DB_PORT:", os.getenv('DB_PORT'))
    print("DB_USER:", os.getenv('DB_USER'))
    print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
    print("DB_NAME:", os.getenv('DB_NAME'))

    # Connexion à la BDD
    conn = mysql.connector.connect(
        host=os.getenv('DB_HOST'), 
        port=os.getenv('DB_PORT'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD'),
        database=os.getenv('DB_NAME')
    )

    # STRUCTURE DE LA TABLE countries :
    # CREATE TABLE `emissions_by_country` ( `country_name` VARCHAR(255) NOT NULL, `territorial_approach` DOUBLE NULL, `territorial_approach_by_inhabitant` DOUBLE NULL, `consumption_approach` DOUBLE NULL ) ENGINE = InnoDB


    cursor = conn.cursor()

    # Préparer requête d'insertion
    insert_query = "INSERT INTO emissions_by_country (country_name, territorial_approach, territorial_approach_by_inhabitant, consumption_approach) VALUES (%s, %s, %s, %s)"

    # Insérer les données
    for row in structured_data:
        cursor.execute(insert_query, row)

    # Valider les modifications
    conn.commit()

    cursor.close()
    conn.close()

    print("Insertion réussie.")

# Exemple d'utilisation des fonctions :
if __name__ == "__main__":
    raw_data = scrapping_wikipedia_data()
    structured_data = clean_and_structure_data(raw_data)
    enregistrer_en_bdd(structured_data)
