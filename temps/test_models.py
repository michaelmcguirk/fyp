from django.test import Client
import unittest
from django.contrib.auth.models import User
from .models import Temps, Batch, CurrentTemp

class SimpleTest(unittest.TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = "TestingUser", password="password", email="mail@mail.com")
        self.batch = Batch.objects.create(batch_name="TestingBatch")
        self.temps = Temps.objects.create(batch_id = self.batch, tempc = 1, tempf = 1, timestp = "2016-03-16 00:00:00", seq_no = 1)

    def tearDown(self):
        del self.user
        del self.batch
        del self.temps

    def test_temps(self):
        self.batch = Batch.objects.get(batch_name="TestingBatch")
        self.assertEqual(self.batch.batch_name,"TestingBatch")
