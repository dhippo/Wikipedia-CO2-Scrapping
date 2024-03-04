from scraper import scrapping_wikipedia_data
from data_cleaner import clean_and_structure_data, structure_raw_data
from database import enregistrer_en_bdd

if __name__ == "__main__":
    raw_data = scrapping_wikipedia_data()
    structured_data = structure_raw_data(raw_data)
    cleaned_data = clean_and_structure_data(structured_data)
    enregistrer_en_bdd(cleaned_data)
