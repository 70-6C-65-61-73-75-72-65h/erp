import numpy as np
import matplotlib.pyplot as plt


import datetime
import time
import os
import django
import sys

#   data :   [0], range(0, 1), 0, 1
#   
def draw(data1, time1, data2):#, data_max, time_max, today): , data2, time2
    try:
        # fig = plt.figure()
        # # ax1 = fig.add_subplot(211)
        # fig.set_ylabel('number of purchases')
        # fig.set_xlabel('days')
        # fig.set_title('Purchase number progression')
        # fig.plot(time1, data1)
        # # beautify the x-labels
        # fig.gcf().autofmt_xdate()

        # fig.savefig('Purchases.png')

        fig = plt.figure()
        # fig.subplots_adjust(top=1.0)
        ax1 = fig.add_subplot(211)
        ax1.set_ylabel('number of purchases')
        ax1.set_xlabel('days')
        ax1.set_title('Purchase number progression')
        ax1.plot(time1, data1)
        # plt.plot(time1, data1)
        # fig.suptitle('Purchase number progression', fontsize=20)
        # plt.xlabel('days', fontsize=18)
        # plt.ylabel('number of purchases', fontsize=16)

        ax2 = fig.add_subplot(212)
        ax2.set_ylabel('number of assets/passives')
        ax2.set_xlabel('days')
        ax2.set_title('Assets/Passives number progression')
        ax2.plot(time1, data2)
        # plt.plot(time1, data2)
        # fig.suptitle('Assets/Passives number progression', fontsize=20)
        # plt.xlabel('days', fontsize=18)
        # plt.ylabel('number of assets/passives', fontsize=16)

        plt.gcf().autofmt_xdate()
        fig.savefig('Frame10.png')
        # fig.savefig('Assets.png')

        # ax2 = fig.add_subplot(212)
        # ax2.set_ylabel('number of warehouse transfers')
        # ax2.set_xlabel('days')
        # ax2.set_title('Warehouse transfers number progression')
        # ax2.plot(time2, data2)
        # # beautify the x-labels
        # ax1.gcf().autofmt_xdate()

        # fig2 = plt.figure()

        # # ax2 = fig.add_subplot(212)
        # fig2.set_ylabel('number of assets/passives')
        # fig2.set_xlabel('days')
        # fig2.set_title('Assets/Passives number progression')
        # fig2.plot(time1, data2)
        # # beautify the x-labels
        # fig2.gcf().autofmt_xdate()

        # fig2.savefig('Assets.png')

    except Exception as ex:
        print('\n\nError')
        print(ex)

    # print(f'data : \t {data}, {time}, {data_max}, {time_max}')
    # fig, ax = plt.subplots()
    # line, = ax.plot(data, time, color='k')
    # # for n in range(len(x)):
    # for x, y in zip(data, time):
    #     line.set_data(x, y)
    #     # line.set_data(x, (today - datetime.timedelta(len(time)-y)))
    # print('\n\ndef draw there\n\n')
    # # if data_max == 0:# or time_max == 0:
    # #     ax.axis([0, 1, (today - datetime.timedelta(1)), today])
    # # # elif data_max == 0:
    # # #     ax.axis([0, 1, 0, 1])
    # # else:
    # #     ax.axis([0, data_max, 0, time_max])
    # if data_max == 0:
    #     ax.axis([0, 1, time[0], time_max])
    # else:
    #     ax.axis([0, data_max, time[0], time_max])
    # fig.canvas.draw()
    # fig.savefig('Frame0.png')


def to_pc_graph(yesterday):
    # за предыдущий день - так у нас цикл идет постоянно и быстрее увидин начало дня чем состоится покупка
    pcs = PurchaseClaim.objects.all().filter(created=yesterday).count() # за время периода (до expire_day колличества) (2-3)
    return pcs

def to_ass_pass_graph(yesterday):
    ab = AccountingBalance.objects.all().last()
    assets = ab.get_assets().filter(operative_day=yesterday).count() if ab.get_assets() is not None else 0
    # print(f'\nassets: {assets}')
    # passives = ab.get_passives().filter(operative_day=yesterday) if ab.get_passives() is not None else 0
    return assets#[assets, passives]
# def to_wht_graph(sim):
#     whts = WHTransferClaim.objects.all().filter(created=sim.today).count()
#     return whts
import time
import datetime
def main():
    while 1:
        if simulation.models.Simulation.objects.all().exists():
            break
    sim = simulation.models.get_simulation()
    print('\n\nGRAPH we here!!!!!\n\n')
    print(f'{sim}')
    print(f'{sim.status}')
    while 1:
        time.sleep(1)
        sim.refresh_from_db()
        if sim.status == True:
            break
    print('\n\nGRAPH we here 2!!!!!\n\n')
    data_set_pc = []
    # data_set_wht = []
    today_performed = False
    today = None
    yesterday = None
    data_set_days = []

    data_ass_pass = []
    while 1:
        if not today_performed:
            # print('\n\nHERE graph\n\n')
            today = sim.today
            yesterday = today - datetime.timedelta(1)
            data_set_pc.append(to_pc_graph(yesterday))
            # data_set_wht.append(to_wht_graph(sim))
            # список значений \\ список дат \\ максимальное значение для рамни значений \\ -\\- дат
            # draw(data_set_pc, range(len(data_set_pc)), max(data_set_pc), len(data_set_pc), today) # data and time
            data_set_days.append(yesterday)
            data_ass_pass.append(to_ass_pass_graph(yesterday))
            # print(f'\n\ndata_ass_pass: {data_ass_pass}')
            draw(data_set_pc, data_set_days, data_ass_pass)#, max(data_set_pc), max(data_set_days), today)
            # draw(data_set_wht)
        sim.refresh_from_db()
        today_performed = True if sim.today == today else False


if __name__ == '__main__':
    # print("Starting population script...")
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'erp.settings')
    django.setup()
    from company_operations.models import PurchaseClaim, WHTransferClaim
    from general_accounting.models import AccountingBalance
    import simulation
    main()
