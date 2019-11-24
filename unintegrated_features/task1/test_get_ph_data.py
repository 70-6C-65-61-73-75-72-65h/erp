# import unittest
# from unittest.mock import patch, Mock
# import pickle
# import os

# from get_ph_data import read_apt_matrix, read_apt_names_matrix

# class TestGetPhData(unittest.TestCase):
#     """ матрица создана если можно прочитать значения из созданых ею файлов"""
#     @patch('get_ph_data.create_matrix', return_value=read_apt_matrix)
#     def test_create_matrix(self):


# BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# def read_uprgated_routes():
#     with open((BASE_DIR+r'\diplom\GoogleMaps\for_algs\uprgated_routes_seconds.pickle'), 'rb') as f:
#         data = pickle.load(f)
#     return data
# print(read_uprgated_routes())