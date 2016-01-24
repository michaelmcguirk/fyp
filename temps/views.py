from django.shortcuts import render
from django.http import HttpResponse
from .models import CurrentTemp


def index(request):
	ct = CurrentTemp.objects.order_by('timestp')[0]
	context = {'ct' : ct}
	return render(request, 'temps/index.html', context)

# Create your views here.
