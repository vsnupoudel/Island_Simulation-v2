from multiprocessing import Pool
import numpy as np

def return_numbers():
    return 999
def return_numbers1():
    return 9999

def process_image(num):
    print("Before: =========================================================",
          num.__str__)
    # print(return_numbers())
    # print(return_numbers1())
    print("After: =========================================================", num)


if __name__ == '__main__':
    pool = Pool(8)
    pool.map(process_image, [1,2,3,4,5,6,7,8,9,0,1,2,3,4,5,5,6,7,8,9,0,1,2,4,5,9])