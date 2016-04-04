# Michael McGuirk - D13123389
# DT228/4 - Final Year Project

from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator

from django.db import models

class Batch(models.Model):
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
    body_rating = models.IntegerField(blank=True, null=True,
        validators=[MaxValueValidator(5),MinValueValidator(1)])
    taste_rating = models.IntegerField(blank=True, null=True,
        validators=[MaxValueValidator(5),MinValueValidator(1)])
    notes = models.CharField(max_length=100)
    temp_high_c = models.FloatField(blank=True, null=True)
    temp_low_c = models.FloatField(blank=True, null=True)

    def clean(self):
        if self.start_date > self.end_date:
            raise ValidationError('Start date must be before end date')
        if self.temp_low_c > self.temp_high_c:
            raise ValidationError('Lower temperature limit must be less than higher')

    class Meta:
        db_table = 'batch'

class CurrentTemp(models.Model):
    temp_id = models.IntegerField(primary_key=True)
    tempc = models.FloatField(blank=True, null=True)
    tempf = models.FloatField(blank=True, null=True)
    timestp = models.DateTimeField(blank=True, null=True)
    temp_high_c = models.FloatField(blank=True, null=True)
    temp_low_c = models.FloatField(blank=True, null=True)
    current_batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "Current Temp: " +str(self.tempc) + "c at " + str(self.timestp)

    class Meta:
        db_table = 'current_temp'

class Temps(models.Model):
    temp_id = models.AutoField(primary_key=True)
    batch_id = models.ForeignKey(Batch, on_delete=models.CASCADE, null=True)
    tempc = models.FloatField(blank=True, null=True)
    tempf = models.FloatField(blank=True, null=True)
    timestp = models.DateTimeField(blank=True, null=True)
    seq_no = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return "Id: " + str(self.temp_id) + ", Temp_c: " + str(self.tempc) + ", Temp_f: " + str(self.tempf)  + ", Time: " + str(self.timestp)

    class Meta:
        db_table = 'temps'
        ordering = ['timestp']

class UserBatchSettings(models.Model):
    TEMPERATURE_FORMAT = (('C','Celsius'),('F','Faranheit'))
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    def_temp_low = models.FloatField(blank=True, null=True)
    def_temp_high = models.FloatField(blank=True, null=True)
    def_temp_format = models.CharField(max_length=1,choices=TEMPERATURE_FORMAT,default='C')

    def clean(self):
        if self.def_temp_low > self.def_temp_high:
            raise ValidationError('Lower temperature must be less than higher temperature')

    class Meta:
        db_table = 'user_batch_settings'
