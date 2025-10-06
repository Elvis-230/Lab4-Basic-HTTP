import unittest
import json
from app import app, trial_division

class TestFactoringAPI(unittest.TestCase):
    
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
    
    # Test the trial_division function directly
    def test_trial_division_prime(self):
        self.assertEqual(trial_division(7), [7])
        self.assertEqual(trial_division(13), [13])
        self.assertEqual(trial_division(97), [97])
    
    def test_trial_division_composite(self):
        self.assertEqual(trial_division(12), [2, 2, 3])
        self.assertEqual(trial_division(360), [2, 2, 2, 3, 3, 5])
        self.assertEqual(trial_division(100), [2, 2, 5, 5])
    
    def test_trial_division_edge_cases(self):
        self.assertEqual(trial_division(1), [])
        self.assertEqual(trial_division(2), [2])
        self.assertEqual(trial_division(4), [2, 2])
    
    # Test GET endpoint
    def test_factor_get_prime(self):
        response = self.app.get('/factor/17')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['number'], 17)
        self.assertEqual(data['factors'], [17])
        self.assertTrue(data['is_prime'])
    
    def test_factor_get_composite(self):
        response = self.app.get('/factor/12')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['number'], 12)
        self.assertEqual(data['factors'], [2, 2, 3])
        self.assertFalse(data['is_prime'])
    
    def test_factor_get_edge_cases(self):
        # Test 1
        response = self.app.get('/factor/1')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['factors'], [])
        
        # Test 2 (smallest prime)
        response = self.app.get('/factor/2')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['factors'], [2])
        self.assertTrue(data['is_prime'])
    
    # Test POST endpoint
    def test_factor_post_prime(self):
        response = self.app.post('/factor',
                                data=json.dumps({'number': 23}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['number'], 23)
        self.assertEqual(data['factors'], [23])
        self.assertTrue(data['is_prime'])
    
    def test_factor_post_composite(self):
        response = self.app.post('/factor',
                                data=json.dumps({'number': 360}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertEqual(data['number'], 360)
        self.assertEqual(data['factors'], [2, 2, 2, 3, 3, 5])
        self.assertFalse(data['is_prime'])
    
    def test_factor_post_invalid_input(self):
        # Missing number field
        response = self.app.post('/factor',
                                data=json.dumps({}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Invalid number format
        response = self.app.post('/factor',
                                data=json.dumps({'number': 'abc'}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
        
        # Negative number
        response = self.app.post('/factor',
                                data=json.dumps({'number': -5}),
                                content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_home_endpoint(self):
        """Test home endpoint returns API info"""
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.data)
        self.assertIn('message', data)
        self.assertIn('endpoints', data)

if __name__ == '__main__':
    unittest.main()