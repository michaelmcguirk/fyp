from django.test import Client
import unittest
from django.contrib.auth.models import User
from .models import Temps

class SimpleTest(unittest.TestCase):
    
    def setUp(self):
        User.objects.create_user(username = "TestingUser", password="password", email="mail@mail.com")
        Batch.objects.create(batch_name="TestingBatch")
        batch = batch.objects.get()
        Temps.objects.create(batch_id = batch, tempc = 1, tempf = 1, timestp = "", seq_no = 1)

    def test_temps(self):
        


lass Batch(models.Model):
    #batch_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)
    batch_name = models.CharField(max_length=100)
    beer_type = models.CharField(max_length=100)
    volume_l = models.FloatField(blank=True, null=True)
    initial_gravity = models.FloatField(blank=True, null=True)
    final_gravity = models.FloatField(blank=True, null=True)
    initial_temp = models.FloatField(blank=True, null=True)
    body_rating = models.IntegerField(blank=True, null=True)
    taste_rating = models.IntegerField(blank=True, null=True)
    notes = models.CharField(max_length=100)
    temp_high_c = models.FloatField(blank=True, null=True)
    temp_low_c = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = 'batch'
