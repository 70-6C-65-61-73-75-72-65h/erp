import datetime
import time
import os
import django

def change_staff():
    # работа только с 1 единственной === последней симуляцией
    while 1:
        if simulation.models.Simulation.objects.all().exists():
            break
    sim = simulation.models.get_simulation()
    range_hours = range(24)
    print(f'\n\n{sim}\n\n')
    while 1:
        if sim.status == True:
            for h in range_hours:
                # только для arrival_time
                sim.today_time = sim.today_time + datetime.timedelta(hours=1)
                sim.save()
                simulation.up.check_on_WHTransfer(sim.today_time)
                simulation.up.check_purchase_transfer(sim.today_time)
            sim.today = sim.today + datetime.timedelta(days=1)
            sim.save()
            simulation.up.main(sim) # тут изменения все автоматом над уже заполнеными а в erp/_auto/_up.py  - перед этим
        # time.sleep(2)
        # there will start the stuff called simulate_erp() and there are will be all population of models
        # and even user click stop simulation all things after that will be created and saved there
        sim.refresh_from_db()

# Start execution
if __name__ == '__main__':
    print("Starting population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'app.settings')
    django.setup()
    import simulation
    change_staff()