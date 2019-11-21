import json
import logging
import os
import time
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) ##  + all_paterns
import bs4
# "distance": {"text": "108 km", "value": 107991}, 
# "duration": {"text": "1 hour 43 mins", "value": 6197}, 
# "end_address": "Nezalezhnosti Blvd, 11, Brovary, Kyivs'ka oblast, Ukraine, 07400", 
# "end_location": {"lat": 50.5159628, "lng": 30.7972713}, 
# "start_address": "Bul\u02b9var Oleksandriys\u02b9kyy, 95, Bila Tserkva, Kyivs'ka oblast, Ukraine, 09100", 
# "start_location": {"lat": 49.806135, "lng": 30.1039262}, 

# /\/\ Very big Bag - that addresses only for outside pharmacies ( for 1 in town ) is implemented \\ moreover in drow_graph only outter phs is drawed
def get_addresses():
    """ 45 pharms, cause we get first 44 start_address and last 1 end_address
    there are all (45*(45-1)/2 = 990 routes) will be checked (until get nessesary start_address and end_address)

    вместо этого всего можно было просто сделать:

    all_routes = read_apt_routes()
    addrs = set([route["routes"][0]['legs'][0]["start_address"] for route in all_routes])
    addrs.add(all_routes[-1]["routes"][0]['legs'][0]['end_address'])

    но нам нужен порядок адрессов одинаковый всегда
    """
    all_routes = read_apt_routes()
    addrs = []
    for ind, route in enumerate(all_routes):
        checked_addr = route["routes"][0]['legs'][0]["start_address"]
        if checked_addr not in addrs:
            addrs.append(checked_addr)
        if ind == len(all_routes) - 1:
            addrs.append(route["routes"][0]['legs'][0]["end_address"])
    return addrs
    
    # [route["routes"][0]['legs'][0]["start_address"] for route in read_apt_routes()]

# there are creates some kind of order of apts
def choose_data(data):
    for route in data:
        val = route["routes"][0]['legs'][0]
        temp_list = [
            {
            "distance": val["distance"]['value'], # 111111111 
            "duration": val["duration"]['value'],
            "start_address": val["start_address"],
            "end_address": val["end_address"],
            "start_location_lat": val["start_location"]['lat'],
            "start_location_lng": val["start_location"]['lng'],
            "end_location_lat": val["end_location"]['lat'],
            "end_location_lng": val["end_location"]['lng'],
            'route_improvement': '',
            'time_improvement': None,
            'intermediate_address': '',
            'intermediate_location_lat': None,
            'intermediate_location_lng': None,
            }
        ]
        yield temp_list[:]

def collect_data(side): # outside inside
    data = read_apt_routes(side)
    searched_data = []
    for route in choose_data(data):
        searched_data.append(route)
    return searched_data

def get_data():
    try:
        return collect_data("outside"), collect_data("inside")
    except Exception as e:
        logging.error('Error in def get_data():\n', exc_info=True)
        return None

def read_apt_routes(side='outside'): # 'outside','inside'
    if side in ('outside', 'inside'):
        with open(BASE_DIR + r'\diplom\GoogleMaps\for_algs\apt_routes_{0}.json'.format(side)) as f:
            data = json.load(f)
    else:
        raise KeyError("side can be only 'outside' or 'inside'")
    return data

def write_apt_matrix(data, key): # outside
    with open((BASE_DIR + r'\diplom\GoogleMaps\for_algs\apt_matrix_{0}.json'.format(key)), 'w') as f:
        json.dump(data, f)

def read_apt_matrix(key='duration'): # duration distance
    with open((BASE_DIR + r'\diplom\GoogleMaps\for_algs\apt_matrix_{0}.json'.format(key))) as f:
        data = json.load(f)
    return data

def write_apt_names_matrix(data): # outside
    with open((BASE_DIR + r'\diplom\GoogleMaps\for_algs\apt_names_matrix.json'), 'w') as f:
        json.dump(data, f)

def read_apt_names_matrix(): # outside
    with open((BASE_DIR + r'\diplom\GoogleMaps\for_algs\apt_names_matrix.json')) as f:
        data = json.load(f)
    return data

def get_matrix(data):
    matrix_data = data[:]
    # equality for find num of vertexes in graph with awareness of edges
    equality2 = lambda a,b,c: (1 + (b**2-4*a*c)**(1/2))/2*a # dont search negative answer
    size = int(equality2(1, -1, -len(data)*2)) # n*n(-1)/2 where n - ребра -> уровнение чтоб найти size: x^2-x-1980=0
    inf = 10000001
    val_matrix = []
    for i in range(size):
        l = list(range(size))
        l[i] = inf
        if i != size - 1: # if not the last opertarion
            for j in range(size-i-1): # populate right side of matrix
                cell_data = matrix_data.pop(0)
                l[j+i+1]= cell_data[2]# matrix_data[], #matrix_data.pop(0)[2]
        if i != 0:
            for j in range(0,i):
                l[j] = val_matrix[j][i]
        val_matrix.append(l[:])
    return val_matrix

def get_time(func):
    def inner(*args, **kw):
        t1 = time.clock()
        val = func(*args, **kw)
        t2 = time.clock()
        logging.info(f"\n\nit took {t2-t1} seconds to procced\n\n")
        return val
    return inner

# @get_time # 0.0271224
def get_list(data):
    addrs = []
    for i in enumerate(data):
        if i[1][0]['start_address'] not in addrs:
            addrs.append(i[1][0]['start_address'])
        if i[0] == len(data) - 1:
            addrs.append(i[1][0]['end_address'])
    return addrs

def create_matrix(data, key): # key = meters seconds
    if key not in ("distance", "duration"):
        raise KeyError('in (def create_matrix) only "distance", "duration" keys accepted')
    val = [] # 990 # 45*(45-1)/2
    for route in data:
        val.append([route[0]['start_address'], route[0]['end_address'], route[0][key]])
    vals = get_matrix(val)
    # [print(i) for i in vals]
    write_apt_matrix(vals, key)
    write_apt_names_matrix(get_list(data))

def main():
    # logging.basicConfig(level=logging.DEBUG, format='time: %(asctime)s\nprocces_id: %(process)d\nproccesName: %(processName)s\nuser: %(name)s\n%(message)s') # no user and clientip
    logging.basicConfig(level=logging.DEBUG, format='time:\
        {asctime}\nprocces_id: {process}\nproccesName:\
            {processName}\nuser: {name}\n{message}', style='{')
    data_out, data_in = get_data()
    # create_matrix(data_out, 'distance')
    print(data_out)
    create_matrix(data_out, 'duration')

# # def trans_to_list():
# #     return True
    
# # def read_file(path):
# #     with open(path + 'apt_matrix_{0}.json'.format(key)) as f:
# #         data = json.load(f)
# #     return data

# # def setuplog():
# #     logging.basicConfig(level=logging.DEBUG, format='time:\
# #         {asctime}\nprocces_id: {process}\nproccesName:\
# #             {processName}\nuser: {name}\n{message}', style='{')

# # def transform_data(data, funcs):
# #     return map(lambda func: globals(func), funcs)
    
# # def set_func_data(keys, datas):
# #     return tuple(map(lambda key, data: data[key], [keys, datas]))

# # def distribute_data(data, funcs):
# #     return list(map(lambda f: list(map(lambda k: globals()[k](set_func_data(f[k], data)) \
# #         if f[k] is not None elseglobals()[k](), f)), funcs))

# # # apt_routes_{0}.json'.format(side)
# # # если значения в initial_data под ключем итерируемые - сдвигаем их считывания, иначе - просто читаем 
# # # okey we gonna read only outside file
# # def main():
# #     funcs = [{'setuplog': None}, {'read_file': ['main_path', 'file_pathes']}, {'trans_to_list': ['elem_path', 'searched_data']}] # fuck up file_key
# #     initial_data = {'main_path': os.path.dirname(os.path.abspath(__file__)) + 
# #         "\\diplom\\GoogleMaps\\for_algs\\", 'file_pathes': ["apt_routes_outside.json"],
# #         'elem_path': ["routes", 0, "legs", 0]
# #         'searched_data': [["distance", "value"], 
# #         ["duration", "value"], "start_address", "end_address",
# #         ["start_location", "lat"], ["start_location", "lng"],
# #         ["end_location", "lat"], ["end_location", "lng"]],
# #         'matrix_by_elem': ["distance", "duration"],
# #         'unique_names_by': ["start_address", "end_address"]}
# #     return distribute_data(initial_data, funcs)
# # # unique_names_by - какая-то недоразвитая фигня, прям как я

if __name__ == '__main__':
    main()
# # # funcs = [{"func": setuplog, "key": None}, {"func": read_file, "key": ['main_path', 'file_pathes']}, {"func": trans_to_list, "key": ['elem_path', 'searched_data']}]
# # # print(list(map(lambda f: list(map(lambda k: globals()[k], f)), funcs)))

# # # (f[k]) if f[k] is not None else globals()[k]()
# import os
# keys = ['main_path', 'file_pathes']

# datas = {'main_path': os.path.dirname(os.path.abspath(__file__)) + 
#         "\\diplom\\GoogleMaps\\for_algs\\", 'file_pathes': ["apt_routes_outside.json"],
#         'elem_path': ["routes", 0, "legs", 0],
#         'searched_data': [["distance", "value"], 
#         ["duration", "value"], "start_address", "end_address",
#         ["start_location", "lat"], ["start_location", "lng"],
#         ["end_location", "lat"], ["end_location", "lng"]],
#         'matrix_by_elem': ["distance", "duration"],
#         'unique_names_by': ["start_address", "end_address"]}

# print(tuple(map(lambda key: datas[key], keys)))