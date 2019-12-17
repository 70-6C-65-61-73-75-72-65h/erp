from django.shortcuts import render
from django.http import HttpResponseBadRequest
from .models import HireFireCheck, WHTransfer, Purchase, Vehicle
from accounts.models import Vendor
from simulation.models import get_simulation
# Create your views here.
def list_of_hfcs(request):
    hfcs = None
    exists = False
    if HireFireCheck.objects.all().exists():
        hfcs = HireFireCheck.objects.all().values_list('id', flat=True)
        exists = True
    context = {
        "ids" : hfcs,
        "exists": exists
    }

    return render(request, 'hfcs_list.html', context=context)


def certain_hfc(request, id):
    try:
        hfc = HireFireCheck.objects.get(id=id)
        fired_that_month = [[h.id, h.profile.user.username, h.kind] for h in hfc.fired_that_month.all()]
        will_be_fire_next_month = [[h.id, h.profile.user.username, h.kind] for h in hfc.will_be_fire_next_month.all()]
        hired_that_month = [[h.id, h.profile.user.username, h.kind] for h in hfc.hired_that_month.all()]
        num_ftm = len(fired_that_month)
        num_wbf = len(will_be_fire_next_month)
        num_htm = len(hired_that_month)
        context = {
            "next_check" : hfc.next_check,
            "fired_that_month": fired_that_month,
            "will_be_fire_next_month": will_be_fire_next_month,
            "hired_that_month": hired_that_month,
            "num_ftm": num_ftm,
            "num_wbf": num_wbf,
            "num_htm": num_htm,
            }
        return render(request, 'certain_hfc.html', context=context)
    except Exception as ex:
        print(f'certain_hfc error:\n\n{ex}\n\n')
        return HttpResponseBadRequest()


def inventory_tracking_wht_delivery(request):
    context = {}
    if WHTransfer.objects.all().exists():
        if WHTransfer.objects.filter(started=True, performed=False).all().exists():
            whts = WHTransfer.objects.filter(started=True, performed=False).all()
            vehicles_with_data = [[wht.arrival_to_start, wht.arrival_time, wht.used_vehicle_id, wht.from_wh.pharmacy_number, wht.to_wh.pharmacy_number] for wht in whts]
            veh_ids = whts.values_list('used_vehicle_id', flat=True)
            # wh1_2 = [[wht.from_wh, wht.to_wh] for wht in whts]
            vehicals_reaching_info = []
            # vehicals_to_start = []
            # vehicals_to_end = []
            for veh_data in vehicles_with_data:
                # veh = Vehicle.objects.get(id=veh_data[2])
                vehicals_reaching_info.append(f"Vehicle # {veh_data[2]} reach transfer start warehouse number {veh_data[3]} in datetime: {veh_data[0]} and reach transfer end warehouse number {veh_data[4]} in datetime: {veh_data[1]}, now is {get_simulation().today_time}")
            #Vehicles that already transfering products to destination
            Vehs_trans = Vehicle.objects.filter(transfering=True, id__in=veh_ids).all().values_list('id', flat=True)
            # Vehicles that just reaching start destination
            Vehs_not_trans = Vehicle.objects.filter(transfering=False, id__in=veh_ids).all().values_list('id', flat=True)
            # print(f'\n{vehicals_reaching_info}\n')
            context = {
                "purchases": False,
                "objects_exists": True,
    	        "suitable_objects_exists": True,
                "veh_reaching_data": vehicals_reaching_info,
                "transfering_vehicals": Vehs_trans,
                "not_transfering_vehicals": Vehs_not_trans,
            }
        else:
            context = {
                "purchases": False,
                "objects_exists": True,
    	        "suitable_objects_exists": False,
            }
    else:
        context = {
                "purchases":  False,
                "objects_exists": False,
    	        "suitable_objects_exists": False,
            }
    return render(request, 'inventory_tracking.html', context=context)

def inventory_tracking_purchase_delivery(request):
    context = {}
    if Purchase.objects.all().exists():
        if Purchase.objects.filter(started=True, performed=False).all().exists():
            ps = Purchase.objects.filter(started=True, performed=False).all()
            vendor = Vendor.objects.all().last() # only one
            vehicles_with_data = [[p.arrival_to_start, p.arrival_time, p.used_vehicle_id, p.wh.pharmacy_number] for p in ps]
            veh_ids = ps.values_list('used_vehicle_id', flat=True)
            vehicals_reaching_info = []
            # vehicals_to_start = []
            # vehicals_to_end = []
            for veh_data in vehicles_with_data:
                # veh = Vehicle.objects.get(id=veh_data[2])
                vehicals_reaching_info.append(f"Vehicle # {veh_data[2]} reach transfer start vendor organisation {vendor.organisation} warehouse in datetime: {veh_data[0]} and reach transfer end warehouse number {veh_data[3]} in datetime: {veh_data[1]}, now is {get_simulation().today_time}")
            #Vehicles that already transfering products to destination
            Vehs_trans = Vehicle.objects.filter(transfering=True, id__in=veh_ids).all().values_list('id', flat=True)
            # Vehicles that just reaching start destination
            Vehs_not_trans = Vehicle.objects.filter(transfering=False, id__in=veh_ids).all().values_list('id', flat=True)
            # print(f'\n{vehicals_reaching_info}\n')
            context = {
                "purchases": True,
                "objects_exists": True,
    	        "suitable_objects_exists": True,
                "veh_reaching_data": vehicals_reaching_info,
                "transfering_vehicals": Vehs_trans,
                "not_transfering_vehicals": Vehs_not_trans,
            }
        else:
            context = {
                "purchases": True,
                "objects_exists": True,
    	        "suitable_objects_exists": False,
            }
    else:
        context = {
                "purchases": True,
                "objects_exists": False,
    	        "suitable_objects_exists": False,
            }
    return render(request, 'inventory_tracking.html', context=context)