from util import RequestFactory
from util import DownLoad
import time
import urlseed.UrlSeedClzLoader;
import json
import config
from redis import StrictRedis
import  multiprocessing


from multiprocessing import Process,Pool,Queue


classList = urlseed.UrlSeedClzLoader.getSeedClass()
clzMap = urlseed.UrlSeedClzLoader.getClassList()

# requestFactory = RequestFactory(urlSeedList=classList);
redisconet = StrictRedis(host=config.redis["host"] , port=config.redis["port"], db=config.redis["db"], 
  password=config.redis["password"])
def jsonToDict(jsonStr):
    st = bytes.decode(jsonStr[1],"utf-8")
    return json.loads(st)
def entityToDict(entity):
    clzName = entity.__class__.__name__
    dictMap = {}
    keyValue = {}
    dictMap[clzName] = {
        }
    for (k, v) in list_all_member(entity):
        keyValue[k] = v
    dictMap[clzName] = keyValue
    dictStr = json.dumps(dictMap, ensure_ascii=False)
    return dictStr
def list_all_member(entity):
    for name, value in vars(entity).items():
        yield (name, value);
def downData(res):

    d = DownLoad(requestData=res);
    result = d.downData(headers={
        "user-agent": config.user_agent[0]
    }, timeout=60, verify=False);
    if  isinstance(result,list):
        subRequestFactory = RequestFactory(urlSeedList=result)
        for srf in subRequestFactory.requestInstance():
            redisconet.rpush('urlList',entityToDict(srf))
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
            redisconet.rpush('urlList',entityToDict(srf))
        for entity in datas:
            redisconet.rpush('dataList', entityToDict(entity))
            # dataProcessQueue.append(entity)
        for errors in errorDatas:
            redisconet.rpush('errorList', entityToDict(errors))
          
    else:
        return True
    



def p1():
    pool1 = Pool(processes=4)
    # requestFactory = RequestFactory(urlSeedList=classList);

    while  True:
        for k in range(0,10):
            if redisconet.llen("urlList")<=0:
                
                continue
            request =redisconet.brpop("urlList")
            dicts = jsonToDict(request)
            clzKey =""
            
            for key in dicts:
                clzKey = key
                break;
            obj = clzMap[clzKey]()
            
            for k1,v1 in  list_all_member(obj):
                obj.__setattr__(k1,dicts[clzKey][k1])
            time.sleep(1)
            pool1.apply_async(downData,(obj,))
           
    pool1.close()
    pool1.join()
def main():
    urlquene =Queue()
    dataqueue = Queue()
    errorqueue = Queue()
    if redisconet.llen("urlList") == 0:
        requestFactory = RequestFactory(urlSeedList=classList);
        for rf in requestFactory.requestInstance():
            downData(rf)
    process1 = Process(target=p1,args=())
    # process2 = Process(target=p2,args=(urlquene,))
    process1.start()
    # process2.start()
    process1.join()
    # process2.join()


if __name__ == "__main__":
    main()