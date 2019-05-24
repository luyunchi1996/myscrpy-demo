from util import RequestFactory
from util import DownLoad
from multiprocessing import Process,JoinableQueue
seedUrlQueue = JoinableQueue();
requestFactory = RequestFactory();
def requestFactoryProcess():
      for rd in requestFactory.requestInstance():
            seedUrlQueue.put(rd)
            print("set:",rd)
  
      seedUrlQueue.join()
def downLoadProcess(seedUrlQueue):
      while True:
            res = seedUrlQueue.get()
            if res is None:break
            d=DownLoad(requestData=res);
            d.downData();   
            print("get:",res)
            seedUrlQueue.task_done()



def main():
#     r = RequestFactory();
#     for rd in r.requestInstance():
#       pass
   
      downd =Process(target=downLoadProcess,args=(seedUrlQueue,)) 
      downd.start()
      requestFactoryProcess()
      seedUrlQueue.put(None)
      downd.join()
      print('主线程')
      pass
if __name__ == '__main__':
    main()

