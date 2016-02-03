from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import CurrentTemp
from .forms import BatchForm
import temps.services as service

def index(request):
	ct = service.get_current_temp()
	context = {'ct' : ct}
	return render(request, 'temps/index.html', context)

def new_batch(request):
    if request.method == "POST":
        form = BatchForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            # model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('view_batch', pk=model_instance.batch_id)
    else:
        form = BatchForm()

    return render(request, "temps/new_batch.html", {'form': form})

def view_batch(request, pk):
    batch = get_object_or_404(Batch, batch_id=pk)
    return render(request, 'temps/view_batch.html', {'batch' : batch})



# def index(request):
# 	ct = CurrentTemp.objects.order_by('timestp')[0]
# 	context = {'ct' : ct}
# 	return render(request, 'temps/index.html', context)

# Create your views here.
