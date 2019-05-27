from util import RequestFactory
from util import DownLoad
import multiprocessing
from multiprocessing import Process
from multiprocessing import Pool,Queue
import time
import urlseed.UrlSeedClzLoader;
classList = urlseed.UrlSeedClzLoader.getClassList()
requestFactory = RequestFactory(urlSeedList=classList);



def func(res):
    d = DownLoad(requestData=res);
    result = d.downData(headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    },timeout=2);
    if  isinstance(result,list):
        subRequestFactory = RequestFactory(urlSeedList=result)
        return subRequestFactory
    else:
        return True
def seedUrlProcess(subQueue):
    pool = multiprocessing.Pool(processes = 4);
    result=None
    for rd in requestFactory.requestInstance():

         result = pool.apply_async(func,(rd,))
         if isinstance(result.get(),RequestFactory):
             subrf = result.get()
             for rf in subrf.requestInstance():
                 subQueue.put(rf)
    pool.close()
    pool.join()
    pass
def subSeedUrlProcss(q,eFlag):
    pools = multiprocessing.Pool(processes = 4);
    result=None
    while True:
        if eFlag.qsize() >=20:
            print("Quit SubProcess")
            break;
        if q.empty():
            print("subQueneEmpty->",eFlag.qsize())
            eFlag.put(True)
            time.sleep(1)
            continue
        # 清空 emptyFlag
        eFlag = Queue()
        rqData =q.get()
        result = pools.apply_async(func,(rqData,))
        if isinstance(result.get(),RequestFactory):
            subrf = result.get()
            for rf in subrf.requestInstance():
                q.put(rf)
    pools.close()
    pools.join()   




def main():
    subSeedUrlQueue =Queue(); 
    emptyFlag = Queue()
    emptyFlag.put("a")
    print("startmain->",subSeedUrlQueue.empty())
    process1 = Process(target=seedUrlProcess,args=(subSeedUrlQueue,))
    process2 = Process(target=subSeedUrlProcss,args=(subSeedUrlQueue,emptyFlag,))
    process1.start()
    process2.start()
    process1.join();
    process2.join();
    print("main->",subSeedUrlQueue.empty(),subSeedUrlQueue.qsize())
    print ("Sub-process(es) done.")

   
if __name__ == '__main__':
    main()

