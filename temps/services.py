# Services.py

from temps.models import CurrentTemp
from temps.models import Temps
from temps.models import Batch

def get_batch_temps(**filters):
	#Stuff here
	return Temps.objects.filter(**filters)

def get_batch(batch_id=1):
	return Batch.objects.get(batch_id)

def get_current_temp():
	return CurrentTemp.objects.get(temp_id=1)