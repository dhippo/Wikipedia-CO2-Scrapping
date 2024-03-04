# Projet Scraping des émissions de CO2 par pays

Projet simple permettant de récupérer les informations du tableau "Émissions de CO2 dues aux combustibles fossiles des principaux pays en 2015" de la page Wikipedia française **"Gaz à effet de serre"**.
[Lien de la page Wikipedia](https://fr.wikipedia.org/wiki/Gaz_à_effet_de_serre)


### Technologies utilisées
- Python
- Docker
- Librairies Python : requests, beautifulsoup4, mysql-connector-python

# Installation

## (1) Cloner le projet 
```bash
git clone https://github.com/
```

## (2) Ouvrir une BDD locale MAMP ou WAMP
Allumer MAMP ou WAMP sur sa machine locale.

## (3) Créer la BDD et la table 
#### 1ère étape : 
Créer la BDD avec phpMyAdmin (nommée par exemple **carbon-emissions**) avec utf8_general_ci.

#### 2ème étape : 
Créer la table avec 4 champs
```sql
CREATE TABLE `emissions_by_country` (
  `country_name` varchar(255) NOT NULL,
  `territorial_approach` double DEFAULT NULL,
  `territorial_approach_by_inhabitant` double DEFAULT NULL,
  `consumption_approach` double DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
```

## (4) Ouvrir Docker Desktop
Ouvrir l'application de Docker sur la machine locale permettant de suivre les images et les conteneurs en fonctionnement sur la machine.

## (5) Construire l'image Docker
```bash
docker build -t scrappingco2emissions .
```

## (6) Créer un fichier .env
Pour MAMP sur mac, valeurs de base :
```bash
DB_HOST=host.docker.internal
DB_PORT=8889
DB_USER=root
DB_PASSWORD=root
DB_NAME=carbon-emissions
```
Pour WAMP sur windows, valeurs hypothétiques :
```bash
DB_HOST=host.docker.internal
DB_PORT=3306
DB_USER=root
DB_PASSWORD=
DB_NAME=carbon-emissions
```

## (7) Éxecution du script
Attention: il faut être placé dans le répertoire du projet et mettre l'argument --env lors de son exécution.
```bash
docker run --env-file .env scrappingco2emissions
```