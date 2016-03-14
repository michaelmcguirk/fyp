# forms.py

from django.db import models
from django import forms
from django.forms import ModelForm
from .models import Batch, UserBatchSettings
from django.contrib.auth.models import User

class NewBatchForm(ModelForm):
	class Meta:
		model = Batch
		fields = ['start_date', 'end_date', 'batch_name', 'beer_type', 'volume_l', 'initial_gravity', 'initial_temp', 'temp_high_c', 'temp_low_c']



class UserForm(ModelForm):
    password = forms.CharField(
    	widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    email = forms.CharField(
    	widget=forms.EmailInput(attrs={'class': 'form-control'}))

    username = forms.CharField(
    	widget = forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

class UserSettingsForm(ModelForm):

	def_temp_low = forms.FloatField(
    	widget = forms.NumberInput(attrs={'class': 'form-control'}))

	def_temp_high = forms.FloatField(
    	widget = forms.NumberInput(attrs={'class': 'form-control'}))	

	class Meta:
		model = UserBatchSettings
		fields = ['def_temp_low', 'def_temp_high', 'def_temp_format']