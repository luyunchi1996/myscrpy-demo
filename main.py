from util import RequestFactory
from util import DownLoad
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool
import time
requestFactory = RequestFactory();

def func(res):
    d = DownLoad(requestData=res);
    d.downData();


def main():
    for rd in requestFactory.requestInstance():
        func(rd)
    pool = multiprocessing.Pool(processes = 4)
    for rd in requestFactory.requestInstance():
        pool.apply_async(func, (rd, )) 
    pool.close()
    pool.join()   
    print ("Sub-process(es) done.")

if __name__ == '__main__':
    main()

