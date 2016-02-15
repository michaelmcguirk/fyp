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


# class TempChart(charts.Chart):
#     chart_slug = 'temps_chart'
#     columns = (
#         ('datetime', "Date"),
#         ('float', "Temperature"),
#     )

#     def get_data(self):
#         return Temps.objects.values_list('timestp', 'tempc')