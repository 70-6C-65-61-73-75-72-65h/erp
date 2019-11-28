from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.http import HttpResponseBadRequest, HttpResponseRedirect, HttpResponse
from django.urls import reverse

from django.core import serializers

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

# надо будет додумать форму для симуляции а пока пользуемся автозаполнением
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

def simulation_model_inner_data(request):
    simulations_exists = False
    if Simulation.objects.all().exists():
        sim = get_simulation()
        data = [[field.name, getattr(sim, field.name)] for field in sim._meta.get_fields()]
        # data = serializers.serialize("python", data)
        # data = [[key, value] for key, value in data.__dict__.items]
        print(data)
        simulations_exists = True
    context = {
        "simulations_exists": simulations_exists,
        "data": data
    }
    return render(request, "simulation_data.html", context)

def simulation_auto_create(request):
    # integrety error simulation_simulation_pkey
    Simulation.objects.create(
        percent_pre_buy_max_prob=0.7,
        ph_sp_max_prob=0.5,
        dpt_sp_max_prob=0.5,
        v_r_max_prob=0.5,
        product_cost_price_max_prob=0.5,
        d_q_r_max_prob=0.5,
        prob_of_worker_fired_dir=0.001, # помимо того что предлагают на увольнение хр по фармацептами ( собственная вероятность увольнения ) на этот  месяц
        prob_of_worker_fired_hr=0.005,
        prob_of_worker_fired_am=0.005,
        prob_of_worker_fired_sa=0.008,
        prob_of_worker_fired_cl=0.03,
        prob_of_worker_fired_ld=0.004,
        prob_of_worker_fired_dr=0.015,
        prob_of_worker_fired_ph=0.01,
        assesment_range=[1,5],
        prob_of_client_assessment=0.1,
        prob_max_assesm_client=0.8,
        assesm_to_delete_worker=2,
        threshold_bad_assesses=4,
        prob_delete_worker=0.3,

        auto_populated=True,
        percent_pre_buy=[0.4, 0.7],
        today=datetime.date.today(),
        today_time=datetime.datetime.today(),
        minimal_zp=4173,
        pharmacys_sizes=40.0,
        department_size=300.0,
        tax_property_size_limit=60.0,
        pharmacys_spendingds=[300, 500],
        department_spendingds=[3000, 5000],
        veh_repair_price_month=[3000, 6000],
        # vehicles_num=11,
        vehicles_purchase_num=11,
        vehicles_whtransfer_num=4,
        vehicle_name='Ford Transit FT-190L',
        vehicle_price=25000.0,
        fuel_price=28.73,
        fuel_type='A-95',
        vehicle_consumption=9.0,
        delivery_added_time_koef=1.15,
        number_to_dispatch=300,
        normal_purch_days=28,
        threshold_days=7,
        number_of_products_names=60,
        product_markup_rate=[0.25, 0.3],
        product_cost_price=[20.0, 500.0],
        whp_self_rate=[0.7, 1.5],
        whp_quantity=[50, 100],#[100, 200],
        day_quantity_range=[0, 7], # 0, 7 - maybe no one buy it today
        salary_pharmacist=7000.0,
        pharmacist_per_wh=3,
        salary_HR=11000.0,
        HR_num=6,
        salary_accounting_manager=8000.0,
        accounting_manager_num=2,
        salary_director=15000.0,
        salary_cleaner=5000.0,
        cleaner_per_wh=2,
        salary_loader=7000.0,
        loader_per_vehicle=2,
        salary_driver=10000.0,
        driver_per_vehicle=2,
        salary_sys_admin=10000.0,
        sys_admin_num=2,
        num_of_clients=88,
        # for convinience in opening accounts
        that_user_password="that_user_111"
    )
    return HttpResponseRedirect(reverse('simulation:simulation_page'))

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
    