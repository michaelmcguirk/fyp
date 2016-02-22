from django.shortcuts import get_object_or_404
from .models import Temps, Batch
from chartit import DataPool, Chart
import temps.services as service

def temps_chart(batch_id):
	batch_temps = service.get_batch_temps(batch_id=batch_id)
	batch = get_object_or_404(Batch, batch_id=batch_id) 
	temp_data = \
	DataPool(series=[{'options': {'source': batch_temps},'terms': ['timestp','tempc']}])

	chart = Chart(
		datasource = temp_data,
		series_options =
		[{'options':{
			'type': 'line',
			'stacking': False},
			'terms':{
			'timestp': [
			'tempc']
			}}],
			chart_options =
			{'title': {
			'text': 'All temperature readings for: ' + batch.batch_name},
			'xAxis': {
			'title': {
			'text': 'Date / Time'}}})
	return chart

def temps_chart_numbered(batch_temps):
	#batch_temps = service.get_batch_temps(batch_id=batch_id)
	batch = get_object_or_404(Batch, batch_id=1) 
	temp_data = \
	DataPool(series=[{'options': {'source': batch_temps},'terms': ['seq_no','tempc']}])

	chart = Chart(
		datasource = temp_data,
		series_options =
		[{'options':{
			'type': 'line',
			'stacking': False},
			'terms':{
			'seq_no': [
			'tempc']
			}}],
			chart_options =
			{'title': {
			'text': 'All temperature readings for: ' + batch.batch_name},
			'xAxis': {
			'title': {
			'text': 'Date / Time'}}})
	return chart

def google_chart_3(batch_temps):
	data = [['Sequence','Temp']]
	for b in batch_temps:
		data.append([b.seq_no,b.tempc])
	return data

def google_chart(batch_temps):
	data = []
	for b in batch_temps:
		data.append([b.seq_no,b.tempc,b.timestp.strftime("%Y-%m-%d %H:%M:%S")])
	return data