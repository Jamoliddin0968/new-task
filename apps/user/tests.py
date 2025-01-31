from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status

class APITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.send_code_url = 'send-code/'
        self.verify_code_url = 'verify-code/'
        self.register_url = 'register/'

    def test_send_code(self):
        response = self.client.post(self.send_code_url, {'phone': '1234567890'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_code(self):
        # Допустим, код уже сохранён в базе
        response = self.client.post(self.verify_code_url, {'phone': '1234567890', 'code': '1234'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_register_user(self):
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'password': 'password123',
            'phone': '1234567890',
            'role': 'buyer'
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
