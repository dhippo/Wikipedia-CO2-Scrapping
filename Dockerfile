# Utilisez l'image officielle Python comme image de base
FROM python:3.9-slim

# Définissez le répertoire de travail dans le conteneur
WORKDIR /app

# Copiez le fichier requirements.txt dans le conteneur
COPY requirements.txt .

# Installez les dépendances spécifiées dans requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copiez le reste du code source de votre projet dans le conteneur
COPY . .

# Commande par défaut pour exécuter l'application
CMD ["python", "scrapper.py"]
