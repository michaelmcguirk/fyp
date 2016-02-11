# from django_google_charts import charts
# from .models import Temps

# class TempChart(charts.Chart):
#     chart_slug = 'temps_chart'
#     columns = (
#         ('datetime', "Date"),
#         ('float', "Temperature"),
#     )

#     def get_data(self):
#         return Temps.objects.values_list('timestp', 'tempc')