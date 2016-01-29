# Services.py

from temps.models import CurrentTemp
from temps.models import Temps
from temps.models import Batch

def get_batch_temps(batch_id, from_date, to_date):
	#Stuff here
	Batch.objects.filter(batch_id)