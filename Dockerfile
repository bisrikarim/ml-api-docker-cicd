# Dockerfile pour l'API ML
# Multi-stage build pour optimiser la taille de l'image

# Stage 1: Build - Entraînement du modèle
FROM python:3.11-slim as builder

WORKDIR /app

# Installation des dépendances
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copie du script d'entraînement
COPY train_model.py .

# Entraînement du modèle
RUN python train_model.py

# Stage 2: Runtime - API seulement
FROM python:3.11-slim

WORKDIR /app

# Installation uniquement des dépendances runtime (sans scikit-learn de dev)
RUN pip install --no-cache-dir flask==3.0.0 gunicorn==21.2.0 scikit-learn==1.3.2 pandas==2.1.4 numpy==1.26.2

# Copie du modèle entraîné depuis le stage builder
COPY --from=builder /app/models ./models

# Copie de l'application
COPY app.py .

# Exposition du port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD python -c "import requests; requests.get('http://localhost:5000/health')" || exit 1

# Commande de démarrage avec Gunicorn (production-ready)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]

