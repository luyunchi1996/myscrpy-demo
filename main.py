from util import RequestFactory
from util import DownLoad
import time
import urlseed.UrlSeedClzLoader;
import json
from redis import StrictRedis
import  multiprocessing

from multiprocessing import Pool,Queue


classList = urlseed.UrlSeedClzLoader.getClassList()
requestFactory = RequestFactory(urlSeedList=classList);


def func(res):
    d = DownLoad(requestData=res);
    result = d.downData(headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    }, timeout=2, verify=False);

    return  result;


def list_all_member(entity):
    for name, value in vars(entity).items():
        yield (name, value);
def processData(data):
    print("redis in Process :")
    clzName = data.__class__.__name__
    dictMap = {}
    keyValue = {}
    dictMap[clzName] = {
    }
    for (k, v) in list_all_member(data):
        keyValue[k] = v
    dictMap[clzName] = keyValue
    dictStr = json.dumps(dictMap, ensure_ascii=False)
    print(dictStr)
    redisconet = StrictRedis(host='192.168.196.128', port=6380, db=0, password='123456')
    redisconet.rpush('dataList', dictStr)
def processError(data):
    clzName = data.__class__.__name__
    dictMap = {}
    keyValue = {}
    dictMap[clzName] = {
    }
    for (k, v) in list_all_member(data):
        keyValue[k] = v
    dictMap[clzName] = keyValue
    dictStr = json.dumps(dictMap, ensure_ascii=False)
    redisconet = StrictRedis(host='192.168.196.128', port=6380, db=0, password='123456')
    redisconet.rpush('errorList', dictStr)

def main():
    urlQueue = Queue()
    dataProcessQueue = Queue()
    errorDataQuene =Queue()

    waitFlag = []
    datawaitFlag = []

    for rf in requestFactory.requestInstance():
        result = func(rf)
        if isinstance(result, list):
            subRequestFactory = RequestFactory(urlSeedList=result)
            for srf in subRequestFactory.requestInstance():
                urlQueue.put(srf)
        elif isinstance(result, dict):
            urlList = []
            if "urlList" in result:
                urlList = result["urlList"]
            datas = []
            if "datas" in result:
                datas = result["datas"]
            errorDatas = []
            if "errorDatas" in result:
                errorDatas = result["errorDatas"]
            subRequestFactory = RequestFactory(urlSeedList=urlList)
            for srf in subRequestFactory.requestInstance():
                urlQueue.put(srf)
            for entity in datas:
                dataProcessQueue.put(entity)
            for errors in errorDatas:
                errorDataQuene.put(errors)





    while True:
        print("wait...")
        if urlQueue.empty() == 0 and dataProcessQueue.empty() == 0 and errorDataQuene.empty() == 0:
            if len(waitFlag) >= 20:
                break
            waitFlag.append(True)
            time.sleep(1)
            continue
        waitFlag = None
        result1  = []
        pool = multiprocessing.Pool(processes=4);
        print("pool start")
        for i in range(0,10):
            if urlQueue.empty():
                continue
            rq = urlQueue.get()
            result1.append(pool.apply_async(func, (rq,)))
        pool.close()
        pool.join()
        print("pool exit")
        for results in result1:
            result = results.get()
            if isinstance(result, list):
                subRequestFactory = RequestFactory(urlSeedList=result)
                for srf in subRequestFactory.requestInstance():
                    urlQueue.put(srf)
            elif isinstance(result, dict):
                urlList = []

                if "urlList" in result:
                    urlList = result["urlList"]
                datas = []
                if "datas" in result:
                    datas = result["datas"]
                errorDatas = []
                if "errorDatas" in result:
                    errorDatas = result["errorDatas"]
                subRequestFactory = RequestFactory(urlSeedList=urlList)
                for srf in subRequestFactory.requestInstance():
                    urlQueue.put(srf)
                for entity in datas:

                    dataProcessQueue.put(entity)
                for errors in errorDatas:
                    errorDataQuene.put(errors)


        datapool = multiprocessing.Pool(processes=4);
        print("datapool start")
        for i in range(0,10):
            if dataProcessQueue.empty():
                continue
            dpq = dataProcessQueue.get()
            print("dpq")
            datapool.apply_async(processData,(dpq,))
        datapool.close()
        datapool.join()
        print("datapool exit")
        errorpool = multiprocessing.Pool(processes=4);
        print("errorpool start")
        for i in range(0,10):
            if errorDataQuene.empty():
                continue
            edq = errorDataQuene.get()
            errorpool.apply_async(processError, (edq,))
        errorpool.close()
        errorpool.join()
        print("errorpool exit")
    print("end")





if __name__ == '__main__':
    main()