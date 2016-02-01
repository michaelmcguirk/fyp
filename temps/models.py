# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin sqlcustom [app_label]'
# into your database.
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

class CurrentTemp(models.Model):
    temp_id = models.IntegerField(primary_key=True)
    tempc = models.FloatField(blank=True, null=True)
    tempf = models.FloatField(blank=True, null=True)
    timestp = models.DateTimeField(blank=True, null=True)
    temp_high_c = models.FloatField(blank=True, null=True)
    temp_low_c = models.FloatField(blank=True, null=True)

    def __str__(self):
        return "Current Temp: " +str(self.tempc) + "c at " + str(self.timestp)

    class Meta:
        db_table = 'current_temp'


class Batch(models.Model):
    batch_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
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

    class Meta:
        db_table = 'batch'

class Temps(models.Model):
    temp_id = models.AutoField(primary_key=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    tempc = models.FloatField(blank=True, null=True)
    tempf = models.FloatField(blank=True, null=True)
    timestp = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "Id: " + str(self.temp_id) + ", Temp_c: " + str(self.tempc) + ", Temp_f: " + str(self.tempf)  + ", Time: " + str(self.timestp)

    class Meta:
        db_table = 'temps'

class UserSettings(models.Model):
    setting_id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    def_temp_low = models.FloatField(blank=True, null=True)
    def_temp_high = models.FloatField(blank=True, null=True)
    def_temp_format = models.CharField(max_length=1)

    class Meta:
        db_table = 'user_settings'
