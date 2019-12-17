import os
import sys
import time
from multiprocessing.dummy import Pool as ThreadPool

# -u - update # nothing or l - load
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def simulate(up=False):
    file_2 = 'simulative_bgrd_task.py'
    if up:
        file_2 = file_2 + ' -u'
    cores = os.cpu_count()
    # Make the Pool of workers
    pool = ThreadPool(cores)

    files = [
        'manage.py runserver 0.0.0.0:8000',
        file_2,
        'graphics.py'
    ]
    pool.map(lambda file: os.system(file), files)
    #close the pool and wait for the work to finish 
    pool.close()
    pool.join()

def main():
    if len(sys.argv) == 2:
        if sys.argv[1] == '-u':
            try:
                t1 = time.clock()
                os.system(BASE_DIR+r'\_auto\_ddb.py')
                t2 = time.clock()
                print(f'\n\ntables dropping and creation time :{t2-t1} sec\n\n')
                simulate(up=True)
            except Exception as ex:
                print(ex)
    elif len(sys.argv) == 1:
            try:
                simulate()
            except Exception as ex:
                print(ex)

if __name__=='__main__':
    main()