from company_operations.models import perform_sale, check_WHT_arrival, check_purchase_arrival, check_Veh_repair_Payment, check_CommunalServisePayment, check_SalaryPayment

def check_on_WHTransfer(today_time):
    check_WHT_arrival(today_time)

def check_purchase_transfer(today_time):
    check_purchase_arrival(today_time)
    
def main(sim):
    perform_sale(sim) # == perform_day
    check_Veh_repair_Payment()
    check_CommunalServisePayment()
    check_SalaryPayment()

# main(sim)