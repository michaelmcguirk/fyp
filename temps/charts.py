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

def google_chart(batch_temps):
	data = [['Sequence','Temp']]
	for b in batch_temps:
		data.append([b.seq_no,b.tempc])
	return data

def compare_chart(batch_id_a, batch_id_b):
	batch_temps_a = service.get_batch_temps(batch_id=batch_id_a)
	batch_temps_b = service.get_batch_temps(batch_id=batch_id_b)
	batch_a = get_object_or_404(Batch, batch_id=batch_id_a)
	batch_b = get_object_or_404(Batch, batch_id=batch_id_b) 
	temp_data = \
	DataPool(series=[{'options': {'source': batch_temps_a},'terms': [{'timestp_a':'timestp'},{'tempc_a':'tempc'}]},
		{'options': {'source': batch_temps_b},'terms': [{'timestp_b':'timestp'},{'tempc_b':'tempc'}]}
		])

	chart = Chart(
		datasource = temp_data,
		series_options =
		[{'options':{
			'type': 'line',
			'stacking': False},
			'terms':{
			'timestp_a': [
			'tempc_a'],
			'timestp_b': [
			'tempc_b'] 
			}}],
			chart_options =
			{'title': {
			'text': 'All temperature readings for: ' + batch_a.batch_name},
			'xAxis': {
			'title': {
			'text': 'Date / Time'}}})
	return chart

# class TempChart(charts.Chart):
#     chart_slug = 'temps_chart'
#     columns = (
#         ('datetime', "Date"),
#         ('float', "Temperature"),
#     )

#     def get_data(self):
#         return Temps.objects.values_list('timestp', 'tempc')