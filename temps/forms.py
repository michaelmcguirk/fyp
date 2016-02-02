# forms.py

from django.db import Models
from django.forms import ModelForm

class BatchForm(ModelForm):
	class Meta:
		model = Models.Batch
		fields = ['start_date', 'end_date', 'batch_name', 'beer_type']