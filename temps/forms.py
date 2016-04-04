# Michael McGuirk - D13123389
# DT228/4 - Final Year Project

from django.db import models
from django import forms
from django.forms import ModelForm
from django.forms.extras.widgets import SelectDateWidget
from .models import Batch, UserBatchSettings
from django.contrib.auth.models import User

form_control_attr = {'class': 'form-control'}

class NewBatchForm(ModelForm):
    start_date = forms.DateField(
        widget = SelectDateWidget(attrs=form_control_attr))

    end_date = forms.DateField(
        widget = SelectDateWidget(attrs=form_control_attr))

    batch_name = forms.CharField(
        widget = forms.TextInput(attrs=form_control_attr))

    beer_type = forms.CharField(
        widget = forms.TextInput(attrs=form_control_attr))

    volume_l = forms.IntegerField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)

    initial_gravity = forms.FloatField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)

    initial_temp = forms.FloatField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)

    temp_high_c = forms.FloatField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)

    temp_low_c = forms.FloatField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)

    taste_rating = forms.IntegerField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)

    body_rating = forms.IntegerField(
        widget = forms.NumberInput(attrs=form_control_attr),required=False)
    class Meta:
		model = Batch
		fields = ['start_date', 'end_date', 'batch_name', 'beer_type', 
        'volume_l', 'initial_gravity', 'initial_temp', 'temp_high_c', 
        'temp_low_c', 'taste_rating', 'body_rating']



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