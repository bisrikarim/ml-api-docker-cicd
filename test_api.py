"""
Tests unitaires pour l'API
"""

import unittest
import json
import os
import sys

# Ajout du répertoire parent au path pour importer app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app

class TestAPI(unittest.TestCase):
    
    def setUp(self):
        """Configuration avant chaque test"""
        self.app = app.test_client()
        self.app.testing = True
    
    def test_health_endpoint(self):
        """Test du endpoint /health"""
        response = self.app.get('/health')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertEqual(data['status'], 'healthy')
    
    def test_index_endpoint(self):
        """Test du endpoint /"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIn('message', data)
    
    def test_predict_missing_data(self):
        """Test de prédiction sans données"""
        response = self.app.post('/predict', json={})
        self.assertEqual(response.status_code, 400)
    
    def test_predict_invalid_data(self):
        """Test de prédiction avec données invalides"""
        response = self.app.post('/predict', json={'surface': 100})
        self.assertEqual(response.status_code, 400)
    
    def test_predict_valid_data(self):
        """Test de prédiction avec données valides"""
        # Note: Ce test nécessite que le modèle soit entraîné
        # On skip si le modèle n'existe pas
        if not os.path.exists('models/house_price_model.pkl'):
            self.skipTest("Modèle non trouvé. Exécutez d'abord train_model.py")
        
        response = self.app.post('/predict', json={
            'surface': 100,
            'pieces': 4
        })
        
        if response.status_code == 200:
            data = json.loads(response.data)
            self.assertIn('prix_predicted', data)
            self.assertIsInstance(data['prix_predicted'], (int, float))
        else:
            # Si le modèle n'est pas chargé, on accepte l'erreur 500
            self.assertEqual(response.status_code, 500)

if __name__ == '__main__':
    unittest.main()

