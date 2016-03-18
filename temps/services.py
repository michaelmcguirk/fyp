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

def get_chart_data(batch_temps, batch):
	data = []
	temp_high = batch.temp_high_c
	temp_low = batch.temp_low_c
	style = 'point { size: 1; shape-type: circle; fill-color: #a52714; visible: True }'
	for b in batch_temps:
		if(b.tempc > temp_high or b.tempc < temp_low):
			style = 'point { size: 1; shape-type: circle; fill-color: #a52714; visible: True }'
		else:
			style = 'null'
		data.append([b.seq_no,b.tempc,b.timestp.strftime("%Y-%m-%d %H:%M:%S"),style])
	return data

def generate_stars(rating):
	star = '<i class="fa fa-star"></i>'
	hollow_star = '<i class="fa fa-star-o"></i>'
	rating_string = ''
	for i in range(0,5):
		if i < rating:
			rating_string = rating_string + star
		else:
			rating_string = rating_string + hollow_star
	return rating_string


def get_batch(batch_id=1):
	return Batch.objects.get(pk=batch_id)

def get_current_temp():
	return CurrentTemp.objects.get(temp_id=1)

def create_batch():
	return 1

# Set which batch will be associated with all subsequent temperatures being recorded.
def start_batch(batch_id):
	current_temp = get_object_or_404(CurrentTemp, temp_id=1)
	batch = Batch.objects.get(id=batch_id)
	current_temp.current_batch_id = batch
	current_temp.temp_high_c = batch.temp_high_c
	current_temp.temp_low_c = batch.temp_low_c
	current_temp.save(update_fields=['current_batch_id', 'temp_high_c', 'temp_low_c'])

def stop_batch():
	current_temp = get_object_or_404(CurrentTemp, temp_id=1)
	current_temp.current_batch_id = None
	current_temp.save(update_fields=['current_batch_id'])
