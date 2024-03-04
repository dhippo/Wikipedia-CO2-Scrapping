import requests
from bs4 import BeautifulSoup

def scrapping_wikipedia_data():
    url = 'https://fr.wikipedia.org/wiki/Gaz_%C3%A0_effet_de_serre'
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', id='bodyContent').text
        start_index = content.find("Approche consommationt CO2/personne")
        end_index = content.find("Approche territoriale : les émissions sont attribuées au pays sur le territoire duquel elles se produisent.Approche consommation")

        if start_index != -1 and end_index != -1:
            data = content[start_index:end_index]
        else:
            print("Phrases clés non trouvées.")
            data = ""

        lines = [line for line in data.split('\n') if line.strip() != '']
        lines2 = lines[1:]
        return lines2
    else:
        print(f'Erreur récupération page: Code {response.status_code}')
        return []
