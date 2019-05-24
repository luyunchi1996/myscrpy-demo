from util import RequestFactory
from multiprocessing import Process

def main():
    r = RequestFactory();
    for rd in r.requestInstance():
        print(rd)
    
if __name__ == '__main__':
    main()

