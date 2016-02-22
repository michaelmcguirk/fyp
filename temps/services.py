# Services.py
from django.shortcuts import get_object_or_404
from temps.models import CurrentTemp
from temps.models import Temps
from temps.models import Batch

def get_batch_temps(**filters):
	#Stuff here
	batches = Temps.objects.filter(**filters)
	seq = 1
	for b in batches:
		b.seq_no = seq
		seq+=1
	return  batches


def get_batch(batch_id=1):
	return Batch.objects.get(pk=batch_id)

def get_current_temp():
	return CurrentTemp.objects.get(temp_id=1)

def create_batch():
	return 1

# Set which batch will be associated with all subsequent temperatures being recorded.
def start_batch(batch_id):
	current_temp = get_object_or_404(CurrentTemp, temp_id=1)
	current_temp.current_batch_id = Batch.objects.get(batch_id=batch_id)
	current_temp.save(update_fields=['current_batch_id'])

def stop_batch(batch_id):
	current_temp = get_object_or_404(CurrentTemp, temp_id=1)
	current_temp.current_batch_id = None
	current_temp.save(update_fields=['current_batch_id'])
