from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponseBadRequest

import json
import datetime

from .models import Simulation, get_simulation
from .forms import SimulationForm

# Create your views here.


# def simulation_run(request):
#     sim = get_simulation()
#     if sim.status == False:
#         sim.status = True
#         sim.save() # <- there start population of all erp models and then actual erp work simulation
#         # there gonna do all population ( take a lot of time)
#     context = {
#         "days_passed": sim.get_simulation_day(),
#         "simulation_today_str": (sim.today).strftime("%d %B, %Y") # 06/12/18  ->  12 June, 2018
#         "simulation_status": sim.status
#     }
#     # return render(request, 'simulation_page.html', context=context)

def simulation_page(request):
    context = {
		"simulations_exists": Simulation.objects.all().exists(),
	}
    return render(request, 'simulation_page.html', context)

# def populate_simulation():
#     Simulation.objects.create(today=datetime.date.today())

def simulation_create(request):
	form = SimulationForm(request.Simulation or None)
	if form.is_valid():
		instance = form.save(commit=False)
        instance.today = datetime.date.today()
		instance.save()
		return render(request, 'simulation_page.html')
	context = {
		"form": form,
	}
	return render(request, "simulation_form.html", context)


def simulation(request):
    if request.method == 'POST':  #

        data = json.loads(request.body)
        action = data['action'] # 0 or 1 that mean run or stop
        from_url = data['from_url']
    
        sim = get_simulation()

        if action == "0" and sim.status == True:
            sim.status = False
            sim.save()
        elif action == "1" and sim.status == False:
            sim.status = True
            sim.save()

        context = {
            "days_passed": sim.get_simulation_day(),
            "simulation_today_str": (sim.today).strftime("%d %B, %Y") # 06/12/18  ->  12 June, 2018
            "simulation_status": sim.status
        }

        redirect(from_url)
        return JsonResponse(context)
    # return render(request, 'simulation_page.html', context=context)
    return HttpResponseBadRequest()



# def refresh_simulation_info(request):
def current_simulation_info(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        from_url = data['from_url']
        sim = get_simulation()
        context = {
                "days_passed": sim.get_simulation_day(),
                "simulation_today_str": (sim.today).strftime("%d %B, %Y") # 06/12/18  ->  12 June, 2018
                "simulation_status": sim.status
            }
        redirect(from_url)
        return JsonResponse(context)
    return HttpResponseBadRequest()