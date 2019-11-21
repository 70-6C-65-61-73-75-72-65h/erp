# import sys
# sys.path.append(r"C:\Program Files (x86)\Microsoft Visual Studio\Shared\Python36_64\Lib\site-packages\psycopg2")
import psycopg2
# import configparser
import sys, os
# def dbAccess():
    # config = configparser.ConfigParser()
    # config.read('dbAccess.ini')
    # return config.get('Settings', 'dbname'), config.get('Settings', 'user'), config.get('Settings', 'password')
# """
# Drop all tables of database you given.
# """
def do():
    try:
        # автоматически в соответствиями с найстройками берет доступ к бд
        dbname = 'diplom'
        user = 'postgres'
        password = '111'
        conn = psycopg2.connect(f"dbname='{dbname}' user='{user}' password='{password}'") # perFecTpRomE 
        conn.set_isolation_level(0)
    except Exception as ex:
        print("Unable to connect to the database.")
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        print(exc_type, exc_obj, fname, exc_tb.tb_lineno)

    cur = conn.cursor()

    try:
        cur.execute("SELECT table_schema,table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_schema,table_name")
        rows = cur.fetchall()
        for row in rows:
            print ("dropping table: ", row[1])
            cur.execute("drop table " + row[1] + " cascade")
        cur.close()
        conn.close()
    except:
        print ("Error: ", ex)

do()