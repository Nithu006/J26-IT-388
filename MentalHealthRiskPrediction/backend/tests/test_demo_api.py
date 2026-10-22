"""Runtime API tests, without dataset access or fitted/mock prediction results."""
import unittest
from unittest.mock import patch
from fastapi.testclient import TestClient
from backend.app.main import app

class DemoApiTests(unittest.TestCase):
    def setUp(self):
        self.loader = patch('backend.app.main.load_model', return_value=None)
        self.loader.start()
        self.addCleanup(self.loader.stop)
        self.client = TestClient(app)
        self.client.__enter__()
        self.addCleanup(self.client.__exit__, None, None, None)
        self.features = {f'bvec_{i}': 0 for i in range(16)}

    def test_health_and_model_info(self):
        self.assertEqual(self.client.get('/health').json(), {'status':'ok','model_ready':False})
        self.assertIsNone(self.client.get('/model-info').json()['model_version'])

    def test_valid_input_returns_unavailable(self):
        result = self.client.post('/predict', json={'features':self.features})
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json()['detail'], 'Model not trained / unavailable')

    def test_invalid_inputs_are_rejected_without_echo(self):
        for features in ({}, self.features | {'risk_oof':1}, self.features | {'bvec_0':True}, self.features | {'bvec_0':'private-value'}):
            result = self.client.post('/predict', json={'features':features})
            self.assertEqual(result.status_code, 422)
            self.assertNotIn('private-value', result.text)
        self.assertEqual(self.client.post('/predict', json={'features':self.features,'label':1}).status_code, 422)

    def test_cors_restricted(self):
        for origin, allowed in [('http://127.0.0.1:5173',True),('https://unrelated.example',False)]:
            response = self.client.options('/predict', headers={'Origin':origin,'Access-Control-Request-Method':'POST'})
            self.assertEqual('access-control-allow-origin' in response.headers, allowed)

    def test_real_absent_artifact_loader(self):
        from backend.app.services.model_service import load_model
        self.assertIsNone(load_model('ml/artifacts/models/exploratory_vectors', False))
