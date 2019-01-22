from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse
from .models import FBMessages

# Create your tests here.
# class APICallsTests(TestCase):
#
#     def setUp(self):
#         self.client = APIClient()
#         self.fbmessages_data = {'fb_username': 'tester'}
#         self.response = self.client.post(
#             reverse('create'),
#             self.fbmessages_data,
#             format-'json')