"""
Script d'entraînement du modèle ML
Ce script entraîne un modèle simple de prédiction de prix de maisons
basé sur la surface et le nombre de pièces.
"""

import pickle
import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import os

def train_model():
    """
    Entraîne un modèle de régression linéaire simple
    """
    # Génération de données d'exemple (simulation d'un dataset de maisons)
    # En production, tu chargerais un vrai dataset depuis un fichier ou une DB
    data = {
        'surface': [50, 60, 70, 80, 90, 100, 110, 120, 130, 140, 150, 160, 170, 180, 190, 200],
        'pieces': [2, 2, 3, 3, 3, 4, 4, 4, 5, 5, 5, 6, 6, 6, 7, 7],
        'prix': [150000, 180000, 210000, 240000, 270000, 300000, 330000, 360000, 
                 390000, 420000, 450000, 480000, 510000, 540000, 570000, 600000]
    }
    
    df = pd.DataFrame(data)
    
    # Séparation des features (X) et de la target (y)
    X = df[['surface', 'pieces']]
    y = df['prix']
    
    # Split train/test (80/20)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Entraînement du modèle
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    # Évaluation
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    
    print(f"Train Score (R²): {train_score:.4f}")
    print(f"Test Score (R²): {test_score:.4f}")
    
    # Sauvegarde du modèle
    model_dir = 'models'
    os.makedirs(model_dir, exist_ok=True)
    
    model_path = os.path.join(model_dir, 'house_price_model.pkl')
    with open(model_path, 'wb') as f:
        pickle.dump(model, f)
    
    print(f"Modèle sauvegardé dans {model_path}")
    
    return model

if __name__ == '__main__':
    train_model()

