# import requests
# from bs4 import BeautifulSoup

# import re
# import copy

# def main():
#     link = 'https://dtkt.com.ua/documents/dovidnyk/plan_rah/plan-r.html'
#     page = requests.get(link)
#     regex = re.compile(r'(?<=<\/center>)(.*?)<\/tr>')
#     page_html  = " ".join(((page.content).decode("cp1251")).split())
#     from_center_to_td = (regex.search(page_html)).group(1)
#     # classes_regex // subclasses_regex // accounts_regex
#     # d = 2
#     # sss = f'(?<=[^\d](\d{ {d} })[^\d])(.*?)[^<]*'
#     classification_regex = lambda d: re.compile(f'(?<=[^\d](\d{ {d} })[^\d])(.*?)[^<]*')
#     # subclasses_regex = re.compile(r'(?<=[^\d](\d{2})[.\s])(.*?)[^<]*')
#     # accounts_regex = re.compile(r'(?<=[^\d](\d{3})[.\s])(.*?)[^<]*')
#     accounts = {'1_level': {}, '2_level': {}, '3_level': {}}
#     for reg in range(1, 4):
#         sub_acc = {}
#         for m in re.finditer(classification_regex(reg), from_center_to_td):
#             sub_acc[f'{m.group(1)}'] = m.group(0) #.append({f'{m.group(1)}': m.group(0)}) # by index get value -> accounts['1_level']['1'] -> Необоротные активы
#         accounts[f'{reg}_level'] =copy.deepcopy(sub_acc)
#     return accounts
#     # uzhos = classes_regex.findall(from_center_to_td)
#     # print(uzhos)
#     # print(classes_regex.findall(from_center_to_td))
#     # print(subclasses_regex.findall(from_center_to_td))
#     # print(accounts_regex.findall(from_center_to_td))
#     # classes_regex =  re.compile(r'\s*<\s*p\s*>\s*<\s*i\s*>\s*<\s*b\s*>(.*?)<\s*\/b\s*>\s*<\s*\/i\s*>')
#     # classes = (classes_regex.findall(from_center_to_td))
#     # print(classes)
#     # subclasses_regex = re.compile(r'\s*<\s*p\s*>\s*<\s*b\s*>(.*?)<\s*\/b\s*>\s*<\s*p\s*>')
#     # subclasses = (subclasses_regex.findall(from_center_to_td))
#     # print(subclasses)
#     # accounts_regex = re.compile(r'\s*<\s*p\s*>\s*(.*?)\s*<\s*p\s*>')
#     # accounts = (accounts_regex.findall(from_center_to_td))
#     # print(accounts)
#     # list(map(print, classes))
#     # # regex = re.compile()
#     # # from_center_to_td = regex.search(page.content)
#     # # soup = BeautifulSoup(page.content, 'html.parser')
#     # # pretty = soup.prettify()
#     # # from_center_to_td_pretty = regex.search(pretty)
#     # # print(from_center_to_td_pretty.groups())
#     # # from_center_to_td = regex.search((page.content).decode("ISO-8859-1"))
#     # # s = (page.content).decode("ISO-8859-15")
#     # s  = (page.content).decode("cp1251")
#     # s2 = " ".join(s.split()) # split ( выбирает все кроме вайтспейсов ( тоесть их удаляет ) 
#     # # и добавляет в список), который мы складываем джоином с промежутком  1 вайтспейс
#     # from_center_to_td = regex.search(s2)
#     # shit = from_center_to_td.groups()
#     # # nice_shit = shit.encode().decode("ISO-8859-1")
#     # # print(nice_shit)
#     # print(shit)
#     # # print(from_center_to_td_pretty.groups())
#     # # print('\n\n\n')
#     # # print(from_center_to_td.groups() == from_center_to_td_pretty.groups())
    
#     # # # soup = BeautifulSoup(check, 'html.parser')
#     # # center_tag = soup.center()
#     # # soup.find
#     # # print(center_tag)
# main()

# import datetime
# # import
# # d = datetime.
# # me.date.today() - datetime.date(2001, 10, 28)).days)

# d = datetime.date.today()
# d2 = datetime.date(2001, 10, 28)

# print(d2 < d)



# a = datetime.datetime(2014, 2, 3, 18, 18, 42, 66853)
# b = datetime.datetime(2014, 2, 3, 18, 18, 54, 49846)
# c = b-a
# print(c > timedelta(days))

# # today = datetime.datetime.now()
# DD = datetime.timedelta(days=90)
# earlier = today - DD
# earlier_str = earlier.strftime("%Y:%m:%d")
# print(earlier_str)
# # earlier_str = earlier.strftime("%Y%m%d")



# TODO search /\/\

# 01/\/\понижение размерности списков:
# l  = [0,1,2,3,4]
# l2  = [2,1,2,3,4]
# l3 = [[l],[l2]]
# print(l3)
# l4 = sum(sum(l3, []),[])
# print(l4)

# 02/\/\постгрес sql analog of aggregate to django orm agg

# check aggregate
# import psycopg2
# import sys, os
# import random
# from psycopg2.extensions import AsIs
# # from psycopg2.errors import UndefinedColumn, DatatypeMismatch

# def try_decor(func):
#     def inner(*args, **kwargs):
#         func_answer = None
#         try:
#             func_answer = func(*args, **kwargs)
#         except Exception: # UndefinedColumn
#             # ибо UndefinedColumn (если допустим в table_schema ошибка при написании) и 
#             # DatatypeMismatch( не тот тип занчения в таблицу инсертнулся) 
#             # нельзя никак проверить (нет никакого прямого доступа к ошибкам для кетча)
#             # а вот psycopg2.OperationalError( ошибка при подключении например), TypeError, SyntaxError - те что кетчить можно
#             print(f"""DB error in func: "{func.__name__}"
#                 that in module: {func.__module__}
#                 with inner args: {func.__code__.co_varnames[:-1]}
#                 default args: {func.__defaults__}
#                 and return arg: {func.__code__.co_varnames[-1]}\n""")
#             exc_type, exc_obj, exc_tb = sys.exc_info()
#             fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
#             print(exc_obj, exc_type, fname, exc_tb.tb_lineno)
#         return func_answer
#     return inner

# @try_decor
# def db_connection(dbname, user, password):
#     conn = psycopg2.connect(f"dbname='{dbname}' \
#                             user='{user}' \
#                             password='{password}'")
#     conn.set_isolation_level(0)
#     return conn

# @try_decor
# def db_clear(cur):
#     cur.execute("SELECT table_schema,table_name FROM information_schema.tables \
#                 WHERE table_schema = 'public' ORDER BY table_schema,table_name")
#     rows = cur.fetchall()
#     for row in rows:
#         print ("dropping table: ", row[1])
#         cur.execute("drop table " + row[1] + " cascade") 
#     return True

# @try_decor
# def db_create_table(cur):
#     command = \
#     """
#         CREATE TABLE auth_users (
#             id INT NOT NULL PRIMARY KEY,
#             is_active BOOLEAN NOT NULL
#         )
#     """
#     cur.execute(command)
#     return True

# @try_decor
# def db_populate_table(cur, t_range=10):
#     """ populate table with 10 rows by default"""
#     for i in range(t_range):
#         id = i+1
#         is_active = random.choice([True, False])
#         print(f'id = {id}\tis_active = {is_active}')
#         cur.execute(f"""
#             INSERT INTO auth_users (id, is_active)
#             VALUES ({AsIs(id)}, {AsIs(is_active)})
#         """)
#     return True

# @try_decor
# def db_poulate(cur):
#     if db_create_table(cur) is None or db_populate_table(cur) is None:
#         return None
#     else:
#         return True

# @try_decor
# def db_aggregate(cur):
#     """ create tables in the PostgreSQL database"""
#     commands = \
#     ("""
#     SELECT
#         COUNT(id) AS total_users,
#         SUM(CASE WHEN is_active THEN 1 ELSE 0 END) AS total_active_users
#     FROM
#         auth_users;
#     """,
#     """
#     SELECT
#         COUNT(id) AS total_users,
#         COUNT(id) FILTER (WHERE is_active) AS total_active_users
#     FROM
#         auth_users;
#     """)
#     for command in commands:
#         cur.execute(command)
#         rows = cur.fetchall()
#         print('Aggregated values:')
#         for row in rows:
#             print(f'{row}')
#     return True


# def try_agg():
#     conn = db_connection(dbname='checkings', user='postgres', password='111')
#     cur = conn.cursor() if conn is not None else None
#     if cur is None: return None
#     db_clear(cur)
#     if cur is None: return None
#     db_poulate(cur)
#     if cur is None: return None
#     db_aggregate(cur)
#     if cur is None: return None
#     cur.close()
#     conn.close()
#     return True


# if __name__ == '__main__':
#     answer_string = 'aggregation is complited' if try_agg() is not None else 'aggregation is failed'
#     print(answer_string)
# import random
# import numpy as np
# kek = (0.8, 1.2)
# kek2 = random.choice(np.arange(kek[0], kek[1], 0.1))
# print(kek2)

# from decimal import Decimal as D
# kek = 1.9
# d_keke = D(str(kek))
# print(type(d_keke))

# import numpy as np

# data1 = np.ones((1, 16, 16, 3))
# data2 = np.zeros((1, 16, 16, 1))

# # for a1, a2 in zip(data1, data2):
# #     for b1, b2 in zip(a1, a2):
# #         for c1, c2 in zip(b1, b2):
# #             for index, d in enumerate(c2):
# #                 c2[index] = c1[0]

# # print(data2)
# # print(int(1.2))

# for a1, a2 in zip(data1, data2):
#     for b1, b2 in zip(a1, a2):
#         for c1, c2 in zip(b1, b2):
#             c2[0] =  (c1[0] + c1[1] + c1[2])/3
#             # for index, d in enumerate(c2):
#             #     c2[index] = c1[0]
# print(data2)