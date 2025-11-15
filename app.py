"""
API Flask pour servir le modèle ML
Cette API expose des endpoints pour faire des prédictions de prix de maisons
"""

from flask import Flask, request, jsonify
import pickle
import os
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Chargement du modèle au démarrage
MODEL_PATH = 'models/house_price_model.pkl'

try:
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)
    logger.info(f"Modèle chargé depuis {MODEL_PATH}")
except FileNotFoundError:
    logger.error(f"Modèle non trouvé dans {MODEL_PATH}")
    model = None

@app.route('/health', methods=['GET'])
def health():
    """Endpoint de health check"""
    return jsonify({
        'status': 'healthy',
        'model_loaded': model is not None
    }), 200

@app.route('/predict', methods=['POST'])
def predict():
    """
    Endpoint de prédiction
    Accepte un JSON avec 'surface' et 'pieces'
    Retourne la prédiction du prix
    """
    if model is None:
        return jsonify({
            'error': 'Modèle non chargé. Entraîne d\'abord le modèle.'
        }), 500
    
    try:
        # Récupération des données depuis la requête
        data = request.get_json()
        
        # Validation des données
        if not data:
            return jsonify({'error': 'Aucune donnée fournie'}), 400
        
        surface = data.get('surface')
        pieces = data.get('pieces')
        
        if surface is None or pieces is None:
            return jsonify({
                'error': 'Les champs "surface" et "pieces" sont requis'
            }), 400
        
        # Conversion en float
        surface = float(surface)
        pieces = float(pieces)
        
        # Prédiction
        prediction = model.predict([[surface, pieces]])[0]
        
        logger.info(f"Prédiction: surface={surface}, pieces={pieces}, prix={prediction:.2f}")
        
        return jsonify({
            'surface': surface,
            'pieces': pieces,
            'prix_predicted': round(prediction, 2)
        }), 200
        
    except Exception as e:
        logger.error(f"Erreur lors de la prédiction: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/', methods=['GET'])
def index():
    """Page d'accueil avec documentation"""
    return jsonify({
        'message': 'API de prédiction de prix de maisons',
        'endpoints': {
            'GET /health': 'Vérifier l\'état de l\'API',
            'POST /predict': 'Faire une prédiction (body: {"surface": 100, "pieces": 4})'
        }
    }), 200

if __name__ == '__main__':
    # Port par défaut 5000, peut être surchargé via variable d'environnement
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

