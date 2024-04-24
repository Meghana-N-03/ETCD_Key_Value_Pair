import unittest
from app import app, put_key_value_pair, get_value_for_key, delete_key, list_all_keys

class TestApp(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

        # Put a key-value pair before running each test
        key = 'test_key'
        value = 'test_value'
        put_key_value_pair(key, value)

    def test_put_value(self):
        key = 'test_key'
        value = 'test_value'
        response = self.app.post('/put', data={'key': key, 'value': value})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"successfully added", response.data)
        print(f"Put test: Key='{key}', Value='{value}' -> {response.data.decode()}")
    def test_get_value(self):
        key = 'test_key'
        response = self.app.post('/get', data={'key': key})
        self.assertEqual(response.status_code, 200)
        response_data = response.data.decode()
        if "Key doesn't exist" not in response_data:
            print(f"Get test: Key='{key}', Retrieved Value -> {response_data}")
        else:
            print(f"Get test: Key='{key}' -> Key not found")

    def test_delete_key(self):
        key = 'test_key'
        response = self.app.post('/delete', data={'key': key})
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"successfully deleted", response.data)
        print(f"Delete test: Key='{key}' -> {response.data.decode()}")

if __name__== '_main_':
    unittest.main()