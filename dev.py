from util import RequestFactory
from util import DownLoad
import time
import urlseed.UrlSeedClzLoader;
import json
from redis import StrictRedis
import config




classList = urlseed.UrlSeedClzLoader.getSeedClass()
requestFactory = RequestFactory(urlSeedList=classList);

def func(res,urlQueue,dataProcessQueue,errorDataQuene):
    d = DownLoad(requestData=res);
    result = d.downData(headers={
        "user-agent": config.user_agent[0]
    },timeout=60,verify=False);

    if  isinstance(result,list):
        subRequestFactory = RequestFactory(urlSeedList=result)
        for srf in subRequestFactory.requestInstance():
            urlQueue.append(srf)
    elif isinstance(result,dict):
        urlList=[]
        if "urlList" in  result:
            urlList = result["urlList"]
        datas=[]
        if "datas" in result:
            datas = result["datas"]
        errorDatas=[]
        if "errorDatas" in result:
            errorDatas = result["errorDatas"]
        subRequestFactory = RequestFactory(urlSeedList=urlList)
        for srf in subRequestFactory.requestInstance():
            urlQueue.append(srf)
        for entity in datas:
            dataProcessQueue.append(entity)
        for errors in errorDatas:
            errorDataQuene.append(errors)

    else:
        return True



def list_all_member(entity):
    for name,value in vars(entity).items():
          yield (name,value);
def main():
    urlQueue = []
    dataProcessQueue=[]
    errorDataQuene=[]

    waitFlag = []
    datawaitFlag = []
    redis = StrictRedis(host=config.redis["host"] , port=config.redis["port"], db=config.redis["db"], 
  password=config.redis["password"])


    for rf in requestFactory.requestInstance():
        func(rf,urlQueue,dataProcessQueue,errorDataQuene)
    while True:
        print("wait...")
        if len(urlQueue) == 0 and len(dataProcessQueue) == 0 and  len(errorDataQuene) == 0 :
            if len(waitFlag)>=20:
                 break
            waitFlag.append(True)
            time.sleep(1)
            continue



        print(dataProcessQueue)

        for data in dataProcessQueue:
            clzName = data.__class__.__name__
            dictMap={}
            keyValue = {}
            dictMap[clzName] = {

            }
            for (k,v) in list_all_member(data):
                keyValue[k] = v
            dictMap[clzName] = keyValue
            dictStr = json.dumps(dictMap,ensure_ascii=False)
            redis.rpush('dataList', dictStr)
            print(data)
        for data in errorDataQuene:
            clzName = data.__class__.__name__
            dictMap = {}
            keyValue ={}
            dictMap[clzName] = {
            }
            for (k, v) in list_all_member(data):
                keyValue[k] = v
            dictMap[clzName] = keyValue
            dictStr = json.dumps(dictMap, ensure_ascii=False)
            redis.rpush('errorList', dictStr)
            print(data)


        if len(urlQueue) != 0:
            rd = urlQueue.pop()
            func(rd,urlQueue,dataProcessQueue,errorDataQuene)
       
    print("end")
if __name__ == '__main__':
    main()