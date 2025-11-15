# ML API avec Docker et CI/CD

Un projet simple pour apprendre les bases du MLOps. On a une API Flask qui sert un modèle de machine learning pour prédire le prix de maisons basé sur la surface et le nombre de pièces.

## Ce que fait ce projet

L'idée est simple : tu envoies la surface et le nombre de pièces d'une maison, et l'API te retourne une estimation du prix. Le modèle est entraîné avec des données d'exemple, mais la structure est la même que ce que tu utiliserais en production.

## Structure du projet

- `train_model.py` : Script qui génère des données d'exemple et entraîne un modèle de régression linéaire. Le modèle est sauvegardé dans `models/house_price_model.pkl`
- `app.py` : L'API Flask qui charge le modèle et expose des endpoints pour faire des prédictions
- `Dockerfile` : Build multi-stage qui entraîne le modèle puis crée une image légère pour l'API
- `.github/workflows/ci.yml` : Pipeline GitHub Actions qui teste et build automatiquement à chaque push
- `test_api.py` : Tests unitaires basiques pour vérifier que l'API fonctionne

## Installation et utilisation locale

D'abord, crée un environnement virtuel pour éviter les conflits avec tes autres projets Python :

```bash
python3 -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Ensuite, entraîne le modèle :

```bash
python train_model.py
```

Ça va créer le fichier `models/house_price_model.pkl` qui contient le modèle entraîné.

Pour lancer l'API en local :

```bash
python app.py
```

L'API tourne sur `http://localhost:5000`. Tu peux tester avec curl :

```bash
# Health check
curl http://localhost:5000/health

# Faire une prédiction
curl -X POST http://localhost:5000/predict \
  -H "Content-Type: application/json" \
  -d '{"surface": 100, "pieces": 4}'
```

## Build et déploiement avec Docker

Le Dockerfile utilise un build multi-stage. Le premier stage entraîne le modèle, le second crée une image légère avec juste l'API et le modèle.

Pour builder l'image :

```bash
docker build -t ml-api:latest .
```

Pour lancer le conteneur :

```bash
docker run -p 5000:5000 ml-api:latest
```

Ou avec Docker Compose :

```bash
docker-compose up --build
```

L'API est accessible sur `http://localhost:5000` comme en local.

## CI/CD avec GitHub Actions

Le pipeline s'exécute automatiquement à chaque push sur `main` ou `develop`, ou à chaque pull request.

Il fait deux choses :
1. **Tests** : Installe les dépendances, entraîne le modèle, lance les tests unitaires
2. **Build** : Build l'image Docker et vérifie qu'elle démarre correctement

Si les deux jobs passent, le code est prêt. Tu peux voir les résultats dans l'onglet Actions de GitHub.

## Endpoints de l'API

- `GET /` : Page d'accueil avec la documentation des endpoints
- `GET /health` : Health check pour vérifier que l'API fonctionne et que le modèle est chargé
- `POST /predict` : Faire une prédiction. Body JSON : `{"surface": 100, "pieces": 4}`

## Pourquoi ce projet

C'est un bon point de départ pour comprendre comment mettre un modèle ML en production. On couvre les bases : entraînement, API REST, containerisation, et CI/CD. C'est simple mais ça te donne une base solide pour des projets plus complexes.

## Prochaines étapes possibles

- Ajouter du monitoring avec Prometheus et Grafana
- Déployer sur Kubernetes
- Ajouter un endpoint pour exposer les métriques du modèle
- Implémenter du logging structuré
- Ajouter un cache Redis pour les prédictions fréquentes
- Mettre en place un système de versioning pour les modèles

## Notes techniques

Le modèle utilise scikit-learn avec une régression linéaire simple. En production, tu utiliserais probablement quelque chose de plus sophistiqué, mais le principe reste le même.

L'API utilise Gunicorn en production avec 4 workers. C'est configuré dans le Dockerfile. Pour le développement local, Flask tourne directement.

Les tests sont basiques mais suffisants pour vérifier que l'API répond correctement. Tu peux les étendre selon tes besoins.

