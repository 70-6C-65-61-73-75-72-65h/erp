
def get_trands(product_data):
    pass

def forecast(forecast_data):
    pharmacy_number = wh_forecast_data[0]["wh"]
    # for_each_product = [] # sequence with discret in 1 day for each product
    product_names = [data["product"] for data in forecast_data]
    for_each_product_seq = [[data["saled_quantity"] for data in forecast_data if data["product"]==product] for product in product_names] # все последовательности ежедневного изменения каждого продукта ( по 28-31 длиной )
    
    # return list(map(get_trands, for_each_product_seq)) # demand on each product
    return [0, 0]
