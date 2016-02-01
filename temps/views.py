from django.shortcuts import render
from django.http import HttpResponse
from .models import CurrentTemp
import temps.services as service

def index(request):
	ct = service.get_current_temp()
	context = {'ct' : ct}
	return render(request, 'temps/index.html', context)


# def index(request):
# 	ct = CurrentTemp.objects.order_by('timestp')[0]
# 	context = {'ct' : ct}
# 	return render(request, 'temps/index.html', context)

# Create your views here.
