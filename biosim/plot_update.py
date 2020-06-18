from multiprocessing import Pool
import numpy as np

def return_numbers():
    return 999
def return_numbers1():
    return 9999

def process_image(numbers):
    # for i in range(100):
    print("Before: =========================================================")
    print(return_numbers())
    print(return_numbers1())
    print("After: =========================================================")


if __name__ == '__main__':
    pool = Pool(8)
    pool.map(process_image, range(9999 ))