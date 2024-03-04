# Projet Scraping des émissions de CO2 par pays

Projet simple d'API permettant de récupérer les informations du tableau "Émissions de CO2 dues aux combustibles fossiles des principaux pays en 2015" de la page Wikipedia française **"Gaz à effet de serre"**.
[Lien de la page Wikipedia](https://fr.wikipedia.org/wiki/Gaz_à_effet_de_serre)


### Technologies utilisées
- Python
- Docker
- Librairies Python : requests, beautifulsoup4, sqlalchemy, uvicorn, fastapi



# Base de données
Sur phpMyAdmin
Code pour créer la base de données associée au scrapping
```sql
CREATE TABLE `emissions_by_country` (
  `country_name` varchar(255) NOT NULL,
  `territorial_approach` double DEFAULT NULL,
  `territorial_approach_by_inhabitant` double DEFAULT NULL,
  `consumption_approach` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```
