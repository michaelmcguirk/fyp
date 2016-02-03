# forms.py

from django.db import models
from django.forms import ModelForm
from .models import Batch

class BatchForm(ModelForm):
	class Meta:
		model = Batch
		fields = ['start_date', 'end_date', 'batch_name', 'beer_type']