# forms.py

from django.db import models
from django.forms import ModelForm
from .models import Batch

class NewBatchForm(ModelForm):
	class Meta:
		model = Batch
		fields = ['start_date', 'end_date', 'batch_name', 'beer_type', 'volume_l', 'initial_gravity', 'initial_temp']

class UserSettingsForm(ModelForm):
	class Meta:
		model = UserBatchSettings
		fields = ['def_temp_low', 'def_temp_high', 'def_temp_format']