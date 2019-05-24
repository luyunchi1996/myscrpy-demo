from util import RequestFactory
from util import DownLoad
from multiprocessing import Process,JoinableQueue
import time
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
            # time.sleep(0.2)



def main():

   
      downd =Process(target=downLoadProcess,args=(seedUrlQueue,))
      downd2 =Process(target=downLoadProcess,args=(seedUrlQueue,)) 
      downd3 =Process(target=downLoadProcess,args=(seedUrlQueue,)) 
      downd4 =Process(target=downLoadProcess,args=(seedUrlQueue,)) 
      downd.start()
      downd2.start()
      downd3.start()
      downd4.start()
      
      requestFactoryProcess()
      seedUrlQueue.put(None)
      downd.join()
      downd2.join()
      downd3.join()
      downd4.join()
      print('主线程')
      pass
if __name__ == '__main__':
    main()

