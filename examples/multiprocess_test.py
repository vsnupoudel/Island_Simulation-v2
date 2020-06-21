from multiprocessing import Pool
from examples.recursion_test import return_exp
import os
class Process_Test:
    def __init__(self):
        self.process_ids = []

    def process_function(self):
        for i in range(10):
            pid = os.getpid()
            self.process_ids.append( return_exp() )
            self.process_ids.append(pid)
        self.process_ids = [self.process_ids[i] for _ in range(4)]

def call_process_function_for_all_obj(single_process):
    single_process.process_function()
    print(single_process.process_ids)

if __name__ == '__main__':
    for i in range(100):
        process_object_list = [Process_Test() for _ in range(99) ]
        for proc in process_object_list:
            call_process_function_for_all_obj(proc)

        # pool = Pool(3)
        # pool.map(call_process_function_for_all_obj, process_object_list, 33)
        # pool.close()
        # pool.join()
        print(i, 'this should print when =====================================================')





