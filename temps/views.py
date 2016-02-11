from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import CurrentTemp, Batch, Temps
from .forms import NewBatchForm
import temps.services as service
from chartit import DataPool, Chart

def get_current_temp():
    return service.get_current_temp()

def index(request):
	ct = service.get_current_temp()
	context = {'ct' : get_current_temp()}
	return render(request, 'temps/index.html', context)

def new_batch(request):
    if request.method == "POST":
        form = NewBatchForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            # model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('view_batch', pk=model_instance.batch_id)
    else:
        form = NewBatchForm()

    return render(request, "temps/new_batch.html", {'form': form, 'ct' : get_current_temp()})

def view_batch(request, pk):
    temp_data = \
    DataPool(series=[{'options': {'source': Temps.objects.all()},'terms': ['timestp','tempc']}])

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
                   'text': 'Weather Data of Boston and Houston'},
               'xAxis': {
                    'title': {
                       'text': 'Month number'}}})


    batch = get_object_or_404(Batch, batch_id=pk)
    return render(request, 'temps/view_batch.html', {'batch' : batch, 'ct' : get_current_temp(), 'chart' : chart})

def start_batch(request):
    #context = RequestContext(request)
    batch_id = None
    if request.method == 'GET':
        batch_id = request.GET['batch_id']

    if batch_id:
        service.start_batch(batch_id)

    return HttpResponse(True)




# def index(request):
# 	ct = CurrentTemp.objects.order_by('timestp')[0]
# 	context = {'ct' : ct}
# 	return render(request, 'temps/index.html', context)

# Create your views here.
