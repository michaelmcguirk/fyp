# Michael McGuirk - D13123389
# DT228/4 - Final Year Project
# Class to test view functions in temps/views.py
from django.test import Client
import unittest
from django import test
from .models import UserBatchSettings, Batch, CurrentTemp, Temps
from django.contrib.auth.models import User

class ViewTest(test.TestCase):
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="test", password="test", email="email@mail.com")
        self.client.login(username="test", password="test")
        self.user = User.objects.create_user(username = "TestingUser", password="password", email="mail@mail.com")
        self.batch = Batch.objects.create(batch_name="TestingBatch")
        self.temps = Temps.objects.create(batch_id = self.batch, tempc = 1, tempf = 1, timestp = "2016-03-16 00:00:00", seq_no = 1)
        self.ct = CurrentTemp.objects.create(temp_id=1,tempc=2,tempf=2,timestp="2016-03-16 00:00:00", 
            temp_high_c=2,temp_low_c=1,current_batch_id=self.batch)
        self.settings = UserBatchSettings.objects.create(user_id = self.user,def_temp_low=1,def_temp_high=1)
    
    def tearDown(self):
        del self.client
        #del self.user

    def test_index(self):
        response = self.client.get('/temps/')
        self.assertEqual(response.status_code, 200)

    def test_view_batches(self):
        response = self.client.get('/temps/view_user_batches/' + str(self.user.id) + '/')
        self.assertEqual(response.status_code, 302)

    def test_view_batch(self):
    	response = self.client.get('/temps/view_batch/' + str(self.batch.id) + '/')
    	self.assertEqual(response.status_code, 200)
    	#self.assertEqual(len(response.context['customers']), 5)

    def test_edit_batch(self):
    	response = self.client.get('/temps/edit_batch/' + str(self.batch.id) + '/')
    	self.assertEqual(response.status_code, 200)

    def test_serve_compare_chart(self):
    	response = self.client.get('/temps/serve_compare_chart/' + str(self.batch.id) + '/' + str(self.batch.id) + '/')
    	self.assertEqual(response.status_code, 200)
