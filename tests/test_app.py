import unittest
from app import app

class QuickBiteTests(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_pages(self):
        for path in ['/', '/menu', '/cart', '/confirmation', '/health']:
            self.assertEqual(self.client.get(path).status_code, 200)

    def test_order(self):
        self.client.post('/add/1')
        response = self.client.get('/cart')
        self.assertIn(b'Veg Burger', response.data)
        self.assertIn(b'99', response.data)
        self.client.post('/place-order')
        self.assertIn(b'Your cart is empty', self.client.get('/cart').data)

if __name__ == '__main__':
    unittest.main()
