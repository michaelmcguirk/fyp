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

def create_batch():
	return 1

# Set which batch will be associated with all subsequent temperatures being recorded.
def start_batch(batch_id):
	current_temp = get_object_or_404(CurrentTemp, temp_id=1)
	current_temp.current_batch_id = batch_id
	current_temp.save(update_fields=['current_batch_id'])
