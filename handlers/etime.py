import time
def etime (func):
    def w ():
        start_time = time.time()
        end_time = time.time()
        elapsed_time = end_time - start_time
        print('Elapsed time: ', elapsed_time)

    return w