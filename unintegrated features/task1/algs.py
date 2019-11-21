from collections import deque, namedtuple
import time
import os

import pickle
from get_ph_data import read_apt_matrix, read_apt_names_matrix, collect_data  # without a key
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# doesnt worx with meters

# DEIKSTRA
########################################################################---------------Deikstra`s
# we'll use infinity as a default distance to nodes.
inf = float('inf')
Edge = namedtuple('Edge', 'start, end, cost')

def make_edge(start, end, cost=1):
    return Edge(start, end, cost)

class Graph:
    def __init__(self, edges):
        # let's check that the data is right
        wrong_edges = [i for i in edges if len(i) not in [2, 3]]
        if wrong_edges:
            raise ValueError('Wrong edges data: {}'.format(wrong_edges))
        
        self.edges = [make_edge(*edge) for edge in edges]

        self.vertices = set(sum(([edge.start, edge.end] for edge in self.edges), []))
        self.neighbours = {vertex: set() for vertex in self.vertices}
        for edge in self.edges:
            self.neighbours[edge.start].add((edge.end, edge.cost))

    def get_node_pairs(self, n1, n2, both_ends=True):
        if both_ends:
            node_pairs = [[n1, n2], [n2, n1]]
        else:
            node_pairs = [[n1, n2]]
        return node_pairs

    def remove_edge(self, n1, n2, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        edges = self.edges[:]
        for edge in edges:
            if [edge.start, edge.end] in node_pairs:
                self.edges.remove(edge)

    def add_edge(self, n1, n2, cost=1, both_ends=True):
        node_pairs = self.get_node_pairs(n1, n2, both_ends)
        for edge in self.edges:
            if [edge.start, edge.end] in node_pairs:
                return ValueError('Edge {} {} already exists'.format(n1, n2))

        self.edges.append(Edge(start=n1, end=n2, cost=cost))
        if both_ends:
            self.edges.append(Edge(start=n2, end=n1, cost=cost))

    def dijkstra(self, source, dest):
        assert source in self.vertices, 'Such source node doesn\'t exist'
        distances = {vertex: inf for vertex in self.vertices}
        previous_vertices = {
            vertex: None for vertex in self.vertices
        }
        distances[source] = 0
        vertices = self.vertices.copy()

        while vertices:
            current_vertex = min(
                vertices, key=lambda vertex: distances[vertex])
            vertices.remove(current_vertex)
            if distances[current_vertex] == inf:
                break
            for neighbour, cost in self.neighbours[current_vertex]:
                alternative_route = distances[current_vertex] + cost
                if alternative_route < distances[neighbour]:
                    distances[neighbour] = alternative_route
                    previous_vertices[neighbour] = current_vertex

        path, current_vertex = deque(), dest
        while previous_vertices[current_vertex] is not None:
            path.appendleft(current_vertex)
            current_vertex = previous_vertices[current_vertex]
        if path:
            path.appendleft(current_vertex)
        return (path, distances[dest])      

def populate_lc(list_of_changes):
    search_approp_apts = read_apt_names_matrix() # another package
    for i in list_of_changes:
        i['start_address'] = search_approp_apts[int(i['start_node'])]
        i['intermediate_address'] = search_approp_apts[int(i['new_intermediate_nodes'])]
        i['end_address'] = search_approp_apts[int(i['destination_node'])]


def pre_dei(matrix, all_to_all_time, datas=[]):
    to_graph = []
    fast_search_in_to_graph = {}
    count_for_to_graph_index = 0
    for i in range(len(matrix)):
        for j in range(len(matrix)):
            if i != j:
                fast_search_in_to_graph[str(i), str(j)] = count_for_to_graph_index
                count_for_to_graph_index += 1
                to_graph.append((str(i), str(j), matrix[i][j]))
    graph = Graph(to_graph)
    if not len(datas):
        list_of_changes = []
        set_of_changes = set()
        delete_from_views = set()
        ind_from = to_graph[0][0] # '0'
        t1 = time.clock()
        for i in range(len(matrix)):
            for j in range(len(matrix)):
                if i != j:
                    graph_edge = to_graph[fast_search_in_to_graph[str(i), str(j)]]
                    if graph_edge[0] != ind_from:
                        delete_from_views.add(ind_from)
                        ind_from = graph_edge[0]
                    if (graph_edge[0], graph_edge[1]) not in set_of_changes and \
                        graph_edge[0] not in delete_from_views and \
                            graph_edge[1] not in delete_from_views:
                        new_route = graph.dijkstra(graph_edge[0], graph_edge[1])
                        if new_route[1] < graph_edge[2]:
                            list_of_changes.append({'start_node': new_route[0][0],\
                                 'new_intermediate_nodes': new_route[0][1], \
                                     'destination_node': new_route[0][2], \
                                'saved_time': graph_edge[2] - new_route[1], \
                                    'new_time': new_route[1], 'previous_time': graph_edge[2],\
                                         'start_address':'', \
                                             'intermediate_address':'', 'end_address':''})
                            set_of_changes.add((new_route[0][0],new_route[0][2]))
                            set_of_changes.add((new_route[0][2],new_route[0][0]))
        t2 = time.clock()
        all_to_all_time['deikstra'] = t2 - t1
        #populate
        populate_lc(list_of_changes)
        write_algo_routes_outside(list_of_changes)
        list_of_changes = read_algo_routes_outside() # list of dicts
        return list_of_changes  # ----------------------returned-info------ None or list of dicts
    else:
        if len(datas) != 2: 
            raise Exception('\n\nU use unappropriate call for the \
                fucntion, there is exactly 2 numbers of nodes of the graph required!!\n\n')
        else:
            list_of_changes = []
            t1 = time.clock()
            new_route = graph.dijkstra(str(datas[0]), str(datas[1]))
            t2 = time.clock()
            all_to_all_time['one-to-one_deikstra'] = t2 - t1
            to_graph_edge = to_graph[fast_search_in_to_graph[(str(datas[0]), str(datas[1]))]] 
            if to_graph_edge[2] > new_route[1]:
                list_of_changes.append({'start_node': new_route[0][0], \
                    'new_intermediate_nodes': new_route[0][1], 'destination_node': new_route[0][2], \
                    'saved_time': to_graph_edge[2] - new_route[1], \
                        'new_time': new_route[1], 'previous_time': to_graph_edge[2], \
                            'start_address':'', 'intermediate_address':'', 'end_address':''})
                print('such a big improvement!:\n', list_of_changes[0])
                #populate
                populate_lc(list_of_changes)
            else:
                print('there is no improvement!:\n')
            return list_of_changes # ----------------------returned-info------- None or list of 1 dict
########################################################################---------------Deikstra`s

# FLOYD
########################################################################---------------Floyd`s
# no  source, dest cause there just from all to all
def Floyd(matrix):
    prev_A = [[(matrix[i][j], 0) for j in range(len(matrix[i]))] for i in range(len(matrix))]
    for iteration in range(len(matrix)):
        if iteration > 0:
            prev_A = A[:]
        A = [[(0, 0) for j in range(len(prev_A[0]))] for i in range(len(prev_A))]
        for i in range(len(A)):
            for j in range(len(A[i])):
                if i != j:
                    if prev_A[i][j][0] <= prev_A[i][iteration][0] + prev_A[iteration][j][0]:
                        A[i][j] = prev_A[i][j]
                    else:
                        A[i][j] = (prev_A[i][iteration][0] + prev_A[iteration][j][0], iteration)
    return A

def pre_flo(matrix, all_to_all_time):
    list_of_changes = []
    set_of_changes = set()
    t1 = time.clock()
    floyd_improved_routes = Floyd(matrix)
    for i in range(len(floyd_improved_routes)):
        for j in range(len(floyd_improved_routes)):
            if floyd_improved_routes[i][j][0] != matrix[i][j] and i != j and (i, j) not in set_of_changes:
                list_of_changes.append({'start_node': i, 'new_intermediate_nodes': \
                    floyd_improved_routes[i][j][1], 'destination_node': j, \
                    'saved_time': matrix[i][j]-floyd_improved_routes[i][j][0], \
                        'new_time': floyd_improved_routes[i][j][0], 'previous_time': matrix[i][j], \
                        'start_address':'', 'intermediate_address':'', 'end_address':''})
                set_of_changes.add((i, j))
                set_of_changes.add((j, i))
    t2 = time.clock()
    all_to_all_time['floyd'] = t2 - t1
    #populate
    populate_lc(list_of_changes)
    return list_of_changes  # ----------------------returned-info------------------------- None or list of dicts
########################################################################---------------Floyd`s

def pre_operations():
    matrix = read_apt_matrix() # another package # initial = duration or distance
    all_to_all_time = {}
    # # for floyd
    print('Floyd`s Algorithm per all routes:\n')
    pre_flo(matrix, all_to_all_time)
    # [print(i) for i in pre_flo(matrix, all_to_all_time)]
    # for deixtra
    print('Deikstra`s Algorithm  per all routes:\n')
    pre_dei(matrix, all_to_all_time)
    # [print(i) for i in pre_dei(matrix, all_to_all_time)]
    print('Deikstra`s Algorithm  per one route:\n')
    pre_dei(matrix, all_to_all_time, datas=[0, 19])
    # [print(i) for i in (pre_dei(matrix, all_to_all_time, datas=[0, 19]))]

    print("Виконання Алгоритму Флойда у загальному обсязі склало ",all_to_all_time['floyd']," с\n")
    print("Виконання Алгоритму Дейкстри (пошук усіх маршрутів) у загальному обсязі склало ",all_to_all_time['deikstra']," с\n")
    print("Виконання Алгоритму Дейкстри (один маршрут від {0} до {1} вершини) у загальному обсязі склало ".format(0,1), all_to_all_time['one-to-one_deikstra']," с\n")

    # upgrade initial values of routes between vertexes
    upgrade_routes()


def write_algo_routes_outside(data):
    with open((BASE_DIR+r'\diplom\GoogleMaps\for_algs\algo_routes_outside.pickle'), 'wb') as f:
        pickle.dump(data, f)

def read_algo_routes_outside():
    with open((BASE_DIR+r'\diplom\GoogleMaps\for_algs\algo_routes_outside.pickle'), 'rb') as f:
        data = pickle.load(f)
    return data

def get_intermediate_loc(apt_routes, vert):
    for apt_r in apt_routes:
        if apt_r[0]['start_address'] == vert['intermediate_address']:
            return apt_r[0]["start_location_lat"], apt_r[0]["start_location_lng"]

def upgrade_routes(): # from algs import read_algo_routes_outside
    list_of_changes = read_algo_routes_outside() #list_of_changes always the same
    # list_of_changes_m = read_algo_routes_outside(key='distance')
    print('\n\n', len(list_of_changes),'\n\n')
    apt_routes = collect_data("outside")
    for vert in list_of_changes:
        for route in apt_routes:
            if route[0]['start_address'] == vert['start_address'] and \
                route[0]['end_address'] == vert['end_address']:
                route[0]["route_improvement"] =  f"You should drive through {vert['intermediate_address']}"\
                    f" to improve in duration on {vert['previous_time']-vert['new_time']} seconds"
                route[0]["intermediate_address"] = vert['intermediate_address']
                route[0]["time_improvement"] = vert['previous_time'] - vert['new_time']
                lat, lng = get_intermediate_loc(apt_routes, vert)
                route[0]["intermediate_location_lat"] = lat
                route[0]["intermediate_location_lng"] = lng
    write_uprgated_routes(apt_routes)

def write_uprgated_routes(data):
    with open((BASE_DIR+r'\diplom\GoogleMaps\for_algs\uprgated_routes_seconds.pickle'), 'wb') as f:
        pickle.dump(data, f)

def read_uprgated_routes():
    with open((BASE_DIR+r'\diplom\GoogleMaps\for_algs\uprgated_routes_seconds.pickle'), 'rb') as f:
        data = pickle.load(f)
    return data

#TODO by got names in improvement change routes and write in upgrated_routes_outside


# def get_upgrated():
#     """For graph drawning"""
#     chenged_routes = list(filter(lambda route: route[0]["route_improvement"] != '', read_uprgated_routes()))
#     # list(map(print, chenged_routes))
#     return chenged_routes
# def get_all():


# def main():
#     pre_operations()

# if __name__ == '__main__':
#     main()


##### there just address getting for erp sys with spec alg
pre_dei(read_apt_matrix(), {})
read_uprgated_routes()
pre_flo(read_apt_matrix(), {})
read_uprgated_routes()