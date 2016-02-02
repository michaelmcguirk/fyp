from django.shortcuts import render
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
            # commit=False means the form doesn't save at this time.
            # commit defaults to True which means it normally saves.
            model_instance = form.save(commit=False)
            model_instance.timestamp = timezone.now()
            model_instance.save()
            return redirect('victory')
    else:
        form = MyModelForm()

    return render(request, "temps/new_batch.html", {'form': form})



# def index(request):
# 	ct = CurrentTemp.objects.order_by('timestp')[0]
# 	context = {'ct' : ct}
# 	return render(request, 'temps/index.html', context)

# Create your views here.
