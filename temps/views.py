from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import CurrentTemp, Batch, Temps
from .forms import NewBatchForm, UserForm, UserSettingsForm
import temps.services as service
import temps.charts as charts


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
            return redirect('view_batch', pk=model_instance.id)
    else:
        form = NewBatchForm()

    return render(request, "temps/new_batch.html", {'form': form, 'ct' : get_current_temp()})

def edit_batch(request, pk):
    batch = get_object_or_404(Batch, pk=pk)
    form = NewBatchForm(request.POST, instance=batch)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('view_batch', pk=pk)
    else:
        form = NewBatchForm(instance =batch)

    return render(request, "temps/edit_batch.html", {'form': form, 'ct' : get_current_temp()})

def view_batch(request, pk):
    batch = get_object_or_404(Batch, id=pk)
    batch_temps = service.get_batch_temps(batch_id = pk)
    djangodict = charts.google_chart(batch_temps)

    return render(request, 'temps/view_batch.html', {'batch' : batch, 'ct' : get_current_temp(), 'djangodict' : djangodict})

def view_user_batches(request,pk):
    batches=Batch.objects.filter(user_id=pk)

    return render(request, 'temps/view_user_batches.html', {'batches' : batches, 'ct' : get_current_temp()})

def compare(request, pk):
    batches = Batch.objects.filter(user_id=pk)
    batch = batches[0].id
    batch_a_temps = service.get_batch_temps(batch_id = 2)
    batch_b_temps = service.get_batch_temps(batch_id = 3)
    batch_a = charts.google_chart(batch_a_temps)
    batch_b = charts.google_chart(batch_b_temps)

    return render(request, 'temps/compare.html', {'batch' : batch, 'ct' : get_current_temp(), 'batches' : batches, 'batch_a':batch_a, 'batch_b':batch_b})

def start_batch(request):
    batch_id = None
    if request.method == 'GET':
        batch_id = request.GET['batch_id']

    if batch_id:
        service.start_batch(batch_id)

    return HttpResponse(True)

def stop_batch(request):
    batch_id = None
    if request.method == 'GET':
        batch_id = request.GET['batch_id']

    if batch_id:
        service.stop_batch(batch_id)

    return HttpResponse(True)

def serve_compare_chart(request,b1,b2):
    batch_a = charts.google_chart(service.get_batch_temps(batch_id = b1))
    batch_b = charts.google_chart(service.get_batch_temps(batch_id = b2))
    batch_data = [service.get_batch(b1),service.get_batch(b2)]
    return render(request, 'temps/compare_chart.html', {'batch_a':batch_a, 'batch_b':batch_b, 'batch_data':batch_data})


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        user_settings_form = UserSettingsForm(data=request.POST)

        if user_form.is_valid() and user_settings_form.is_valid():
            # User Instance
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            # Settings Instance
            settings = user_settings_form.save(commit=False)
            settings.user_id = user
            settings.save()

            registered = True
        else:
            print user_form.errors, user_settings_form.errors
    else:
        user_form = UserForm()
        user_settings_form = UserSettingsForm()

    return render(request,'temps/register.html',{'user_form': user_form, 'user_settings_form': user_settings_form, 'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/temps/')
            else:
                return HttpResponse("Account is no longer Active. Likely Disabled... - Contact Admin")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'temps/login.html', {})

