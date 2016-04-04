# Michael McGuirk - D13123389
# DT228/4 - Final Year Project

from django.test import Client
import unittest
from django import test
from django.contrib.auth.models import User
from .models import Temps, Batch, CurrentTemp, UserBatchSettings

class ModelTest(test.TestCase):
    
    def setUp(self):
        self.user = User.objects.create_user(username = "TestingUser", password="password", email="mail@mail.com")
        self.batch = Batch.objects.create(batch_name="TestingBatch")
        self.temps = Temps.objects.create(batch_id = self.batch, tempc = 1, tempf = 1, timestp = "2016-03-16 00:00:00", seq_no = 1)
        self.ct = CurrentTemp.objects.create(temp_id=1,tempc=2,tempf=2,timestp="2016-03-16 00:00:00", 
            temp_high_c=2,temp_low_c=1,current_batch_id=self.batch)
        self.settings = UserBatchSettings.objects.create(user_id = self.user,def_temp_low=1,def_temp_high=1)


    def tearDown(self):
        self.user.delete()
        del self.batch
        del self.temps
        del self.ct
        del self.settings

    def test_batch(self):
        self.batch = Batch.objects.get(batch_name="TestingBatch")
        self.assertEqual(self.batch.batch_name,"TestingBatch")

    def test_temps(self):
        self.temps = Temps.objects.get(timestp = "2016-03-16 00:00:00")
        self.assertEqual(self.temps.timestp.strftime("%Y-%m-%d %H:%M:%S"), "2016-03-16 00:00:00")

    def test_ct(self):
        self.ct = CurrentTemp.objects.get(timestp = "2016-03-16 00:00:00")
        self.assertEqual(self.ct.timestp.strftime("%Y-%m-%d %H:%M:%S"), "2016-03-16 00:00:00")

    def test_settings(self):
        self.settings = UserBatchSettings.objects.get(user_id = self.user)
        self.assertEqual(self.settings.user_id, self.user)