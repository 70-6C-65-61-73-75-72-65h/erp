from company_operations.models import perform_sale, check_WHT_arrival, check_purchase_arrival, check_Veh_repair_Payment, check_CommunalServisePayment, check_SalaryPayment
from general_accounting.models import check_AB_report, check_TB_report



# accounts_vendor

#______________________________________

def import_to_hire_check(sim, style=1):
    from company_operations.models import HireFireCheck
    from accounts.models import Worker
    from mixins.functions import get_binominal
    from mixins.models import Address
    # from simulation.models import get_simulation - ну будет опять импорить потому будет проблемс если далее это вызывать отсюда
    from assessments.models import Assessment
    from django.contrib.auth.models import User
    # from _auto._up import gener_rand_bank_acc

    import random
    import math
    import datetime
    from calendar import monthrange
    import numpy as np


    def gener_rand_bank_acc():
        bank_acc = [str(random.choice(range(0, 10))) for digit in range(16)]
        return ''.join(bank_acc)

    def get_expired_date(sim):
        """ получаем дату месяц назад (приблезительно) """
        that_month_day = sim.today
        days_in_month = monthrange(that_month_day.year, that_month_day.month)[1]
        expired_day = that_month_day - datetime.timedelta(days_in_month)
        return expired_day

    def get_next_date(sim):
        that_month_day = sim.today
        days_in_month = monthrange(that_month_day.year, that_month_day.month)[1]
        day_to_pay = that_month_day + datetime.timedelta(days_in_month)
        return day_to_pay

    def get_bad_workers_phs(sim):
        ws = Worker.objects.filter(kind='pharmacist', fired=False).all()
        workers_to_prob_deletion = []
        for w in ws:
            if Assessment.objects.filter(worker=w, assess__lte=sim.assesm_to_delete_worker, created__gte=get_expired_date(sim)).all().count() >= sim.threshold_bad_assesses:# если плохих оценок больше границы, то проверка на удаление ( но только за этот месяц проверка ассесов)
                workers_to_prob_deletion.append(w)
        return workers_to_prob_deletion

    # тех кого обпределили HR - прямой доступ к FireCheck  - fired_that_month
    def hr_checks_phs(fc, sim):
        """ проверяет каких фармацептов дропнуть и по вероятности дропает"""
        # HireFireCheck.objects.all().last() # удаление задним числом - заносим в старый 
        # fired_that_month.add(Worker.objects.get(id=1))
        workers_delete_acception = get_bad_workers_phs(sim)
        # если абс болшинство спецов по отделу чел рсурсов - за удаление - удаляем в след месяце а пока ищем замену
        for w in workers_delete_acception:
            if get_binominal([1, sim.HR_num + 1], sim.prob_delete_worker) > int((sim.HR_num)/2):
                fc.will_be_fire_next_month.add(w)
        # fc.hired_that_month.save()
        # fc.refresh_from_db()
        fc.save()
        fc.refresh_from_db()
        return fc

    def fire_workers(w_ids): # to fired=True # already added to will be fired in pre month // but in that month just changed the status in own page
        Worker.objects.filter(id__in=w_ids).update(fired=True)
        # just_fired = Worker.objects.filter(id__in=w_ids).all()
        # will_be_fire_next_month

    def create_address(address):
        addr = address.split(',')
        separator = ' /'
        return Address.objects.create(address_line=separator.join(addr[:-4]), city=addr[-4], region=addr[-3], country=addr[-2], postal_code=addr[-1], full_address=address)

    def hire_workers(fc, fw_ids, sim):
        fired_workers = Worker.objects.filter(id__in=fw_ids).all()
        # replace_work_place_ids = Worker.objects.filter(id__in=fw_ids).values_list('id_workon_place', flat=True).order_by('id') # only ids of wh or veh or dpt
        replace_work_place_ids = [[w.kind, w.salary, w.id_workon_place] for w in fired_workers]
        # print(replace_work_place_ids)
        # print()
        for work_id in replace_work_place_ids:
            bank_acc = gener_rand_bank_acc()
            gener_id = gener_rand_bank_acc()
            user = User.objects.create_user(username=f'new_worker_{work_id[0]}_{gener_id}', password=sim.that_user_password)
            user.refresh_from_db()
            user.profile.bank_acc = bank_acc
            user.profile.save()
            worker_address = f'Some_pharmacist#{user.id}_street, Some_house, Some_city, Some_city, Some_counrty, Some_postal_code'
            c_w_a = create_address(worker_address)
            # print(f'created profile: {profile}')
            # print(f'created profile: {user.profile}')
            # print(f'{profile.slug}')
            # print(f'{profile.client}')
            # print(f'{profile.user}')
            # print()
            # print(f'{work_id[0]} ----- {work_id[1]} ------ {work_id[2]}')
            created_worker = user.profile.role_to_worker(kind=work_id[0], salary=work_id[1], address=c_w_a, id_workon_place=work_id[2])
            # print(f'\n\ncreated_worker: {created_worker}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.id}\n\n')
            # created_worker.refresh_from_db()
            # cw = Worker.objects.get(id=created_worker.id)
            # cw2 = Worker.objects.all().last()
            # print(f'\n\n {cw}\n\n')
            # print(f'\n\n {cw2}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.profile}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.salary}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.kind}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.address}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.id_workon_place}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.fired}\n\n')
            # print(f'\n\ncreated_worker: {created_worker.profile}\n\n')
            # error can be there below
            user.profile.save()
            user.refresh_from_db()
            user.profile.refresh_from_db()
            # Worker.objects.get()
            fc.hired_that_month.add(created_worker) #  user.profile.refresh_from_db()
        
        # fc.hired_that_month.save()
        # fc.refresh_from_db()
        fc.save()


    def fired_and_hired_workers(fc, w_ids, sim):
        fire_workers(w_ids)
        hire_workers(fc, w_ids, sim)


    def check_on_be_fired(prob):
        random_shot = random.choice(np.arange(0, 1, 0.01))
        # print(random_shot)
        to_be_fired = True if random_shot <= prob else False
        return to_be_fired
        # print(to_be_fired)

    def check_all_on_fired(fc):
        # sim = get_simulation()
        all_workers_now = Worker.objects.filter(fired=False).all()
        for w in all_workers_now:
            if check_on_be_fired(w.prob_of_worker_fired):
                fc.will_be_fire_next_month.add(w)
        # fc.refresh_from_db()
        # fc.fired_that_month.save()
        fc.save()
        fc.refresh_from_db()
        return fc

        # add to worker model in creationin reciver prob of fire

    def add_previously_fired_workers(fc):
        to_fire_in_that_month = None # list after check may be 
        if HireFireCheck.objects.all().count() > 1: # то проверяем поле по will_be_fire_next_month
            print(f'\n\nHFC: {((HireFireCheck.objects.order_by("id").reverse())[1])} should be id - 1\n\n\n')
            # print(f'HFC: {((HireFireCheck.objects.all().reverse()))}\n\n')
            # to_fire_in_that_month = ((HireFireCheck.objects.all().reverse())[1]).will_be_fire_next_month.all() # penultimate # 12 - 18 дней на поиск замены, потом увольнение
            # print(to_fire_in_that_month)
            to_fire_in_that_month = (HireFireCheck.objects.order_by("id").reverse())[1]#HireFireCheck.objects.get(id=((HireFireCheck.objects.all().last()).id - 1))
            print('\n\n\n тут увольнение\n\n')
            print(to_fire_in_that_month.will_be_fire_next_month.all())
            print('\n\n\n тут увольнение\n\n')
            for w in to_fire_in_that_month.will_be_fire_next_month.all():
                fc.fired_that_month.add(w)
            # fc.refresh_from_db()
            # fc.fired_that_month.save()
            fc.save()
        fc.refresh_from_db()
        return fc


    def update_fire_hire_status_on_workers(fc, sim):
        w_ids = [w.id for w in fc.fired_that_month.all()]

        fired_and_hired_workers(fc, w_ids, sim)


    def perform_fire_checks(sim): # HireFireCheck
        print(f'\n\nIn perform_fire_checks start\n\n')
        # след дату определить для тотальной проверки на увольнение из предприятия
        next_day_to_check_on_fire = get_next_date(sim)
        # print(f'\n{next_day_to_check_on_fire}\n')
        fc = HireFireCheck.objects.create(next_check=next_day_to_check_on_fire)
        print(f'\n{fc}\n')
        fc = add_previously_fired_workers(fc) # add fired_that_month
        # print(f'\nadd_previously_fired_workers\n')
        fc = check_all_on_fired(fc) # and add that will be fired will_be_fire_next_month
        print(f'\ncheck_all_on_fired\n')
        # from asses module func
        fc = hr_checks_phs(fc, sim) # and add that will be fired will_be_fire_next_month
        print(f'\nhr_checks_phs\n')
        update_fire_hire_status_on_workers(fc, sim)
        print(f'\nupdate_fire_hire_status_on_workers\n')
        print(f'\n\nIn perform_fire_checks end\n\n')


    def check_on_perform_fire_checks(sim):
        last_fc = HireFireCheck.objects.all().last()
        if last_fc.next_check <= sim.today:
            perform_fire_checks(sim)





    return check_on_perform_fire_checks(sim) if style == 1 else perform_fire_checks(sim)

    # print(f'\n\nbefore hirefirechecks\n\n')
    # local = locals()
    # print(local)
    # if local['style'] == 1 or style == 1:
    #     print('\n\n\nheeeeeere')
    #     check_on_perform_fire_checks(local['sim'])
    # elif local['style'] == 2 or style == 2:
    #     print(f'\n\nIn hirefirechecks\n\n')
    #     perform_fire_checks(local['sim'])
    
#______________________________________




def check_on_WHTransfer(today_time):
    check_WHT_arrival(today_time)

def check_purchase_transfer(today_time):
    check_purchase_arrival(today_time)



import numpy as np
import matplotlib.pyplot as plt

# def draw(pcs, whts):

#     x = np.linspace(0, 10, 100)
#     y = np.sin(x)

#     fig, ax = plt.subplots()
#     line, = ax.plot(x, y, color='k')

#     for n in range(len(x)):
#         line.set_data(x[:n], y[:n])
#         ax.axis([0, 10, 0, 1])
#         fig.canvas.draw()
#         fig.savefig('Frame0.png')




    
     
def main(sim):
    perform_sale(sim) # == perform_day
    check_Veh_repair_Payment()
    check_CommunalServisePayment()
    check_SalaryPayment()

    check_AB_report(sim.today)
    check_TB_report(sim.today)


    import_to_hire_check(sim)

    # pc_wht_graph(sim)

    # check_on_perform_fire_checks(sim)


def drop_simulation_data():
    from company_operations.models import (CommunalServisePayment, Veh_repair_Payment, 
                    SalaryPayment, Purchase, PurchaseClaim, WHTransfer, WHTransferClaim,
                    Sale, WareHouse, Product, WHProduct, Department, Fuel, Vehicle)
    from general_accounting.models import (Assets, Passives, OperativeAccounts, TaxRate, TrialBalance, AccountingBalance)
    from accounts.models import (Vendor, Worker, Profile, Client)
    from mixins.models import Address
    from assessments.models import Assessment

    CommunalServisePayment.objects.all().delete()
    Veh_repair_Payment.objects.all().delete()
    SalaryPayment.objects.all().delete()
    Purchase.objects.all().delete()
    PurchaseClaim.objects.all().delete()
    WHTransfer.objects.all().delete()
    WHTransferClaim.objects.all().delete()
    Sale.objects.all().delete()
    WareHouse.objects.all().delete()
    Product.objects.all().delete()
    WHProduct.objects.all().delete()
    Department.objects.all().delete()
    Fuel.objects.all().delete()
    Vehicle.objects.all().delete()

    Assets.objects.all().delete()
    Passives.objects.all().delete()
    OperativeAccounts.objects.all().delete()
    TaxRate.objects.all().delete()
    TrialBalance.objects.all().delete()
    AccountingBalance.objects.all().delete()

    Vendor.objects.all().delete()
    Worker.objects.all().delete()
    Profile.objects.all().delete()
    Client.objects.all().delete()

    Address.objects.all().delete()

    Assessment.objects.all().delete()

    
# main(sim)



# perform_fire_checks frm _up.py
# get_clients_assessments