# MNIST Frontend (Streamlit)

Ce dépôt contient la partie frontend (interface Streamlit) du projet de reconnaissance de chiffres manuscrits MNIST.

## Fonctionnalités
- Interface utilisateur pour dessiner un chiffre et obtenir la prédiction.
- Envoie l'image à l'API backend pour la reconnaissance.

## Installation & Lancement

```sh
git clone <ce-repo>
cd mnist-frontend
pip install -r requirements.txt
streamlit run src/app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
```

Ou via Docker :

```sh
docker build -f Dockerfile.streamlit -t mnist-frontend .
docker run -p 8501:8501 mnist-frontend
```

## Séparation front/back
Le frontend est indépendant du backend (API FastAPI). Configurez l'URL de l'API via la variable d'environnement `API_URL` si besoin.

## Arborescence
- `src/app/streamlit_app.py` : code de l'interface Streamlit
- `Dockerfile.streamlit` : image Docker du frontend
- `requirements.txt` : dépendances Python

## Auteur
Votre nom 