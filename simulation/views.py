from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse


import json
import datetime

from .models import Simulation, get_simulation
from .forms import SimulationForm

# Create your views here.

def simulation_page(request):
    context = {
        "simulations_exists": Simulation.objects.all().exists()
	}
    return render(request, 'simulation_page.html', context)

def simulation_create(request):
    form = SimulationForm(request.POST or None)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.today = datetime.date.today()
        instance.save()
        return HttpResponseRedirect(reverse('simulation:simulation_page'))
    context = {
        "form": form,
    }
    return render(request, "simulation_form.html", context)


def simulate(request, action):
    # print('action: ', action)
    sim = get_simulation()
    if action == "disable" and sim.status == True:
        sim.status = False
        sim.save()
    elif action == "enable" and sim.status == False:
        sim.status = True
        sim.save()
    context = {
            "simulations_exists": True,
            "days_passed": sim.get_simulation_day(),
            "simulation_today_str": (sim.today).strftime("%d %B, %Y"), # 06/12/18  ->  12 June, 2018
            "simulation_status": sim.status
    }
    return render(request, "simulation_page.html", context=context)


# def refresh_simulation_info(request):
def current_simulation_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        from_url = data['from_url']
        sim = get_simulation()
        context = {
                "days_passed": sim.get_simulation_day(),
                "simulation_today_str": (sim.today).strftime("%d %B, %Y"), # 06/12/18  ->  12 June, 2018
                "simulation_status": sim.status
            }
        redirect(from_url)
        return JsonResponse(context)
    return HttpResponseBadRequest()
    