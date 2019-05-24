import requests;
import json;
from util.RequestData import RequestData;
from multiprocessing import Process,JoinableQueue;
from util import RequestFactory
import time

downInUrlQueue = JoinableQueue();
requestFactory = RequestFactory();
def requestFactoryProcess():
      for rd in requestFactory.requestInstance():
            downInUrlQueue.put(rd)
      downInUrlQueue.join()
def downLoadProcess(downInUrlQueue):
      while True:
            res = downInUrlQueue.get()
            if res is None:break
            d=DownLoad(requestData=res);
            d.downData();   
            downInUrlQueue.task_done()
            time.sleep(0.2)


class DownLoad():
    data=""
    encoding=""
    def __init__(self,requestData=RequestData(),downQuene=[],encoding="UTF-8"):
        self.encoding = encoding;
        self.requestData = requestData;
        self.byteData='';
        self.state=False
        pass
    def downData(self,retryTimes=3,**kwargs):
        print("download: ",self.requestData.url," params: ",self.requestData.params);
        requestMethods = self.getMethod();
 
        try:
            url = self.requestData.url
            if self.requestData.queryString:
                url+= self.requestData.queryString
            response= requestMethods(url=url,params=self.requestData.params,json=self.requestData.json,data=self.requestData.data,**kwargs)
            response.encoding=self.encoding;
            if response.status_code == 200:
                print("download success");
                self.state = True;
                self.data = response.text;
                self.byteData = response.content;
                if self.requestData.iserror(self.data):
                    parse = self.parseData()
                    self.state = self.requestData.success(parse())
                    print(type(self.state))


                    print()
                    # downd =Process(target=downLoadProcess,args=(downInUrlQueue,))
                    # downd2 =Process(target=downLoadProcess,args=(downInUrlQueue,)) 
                    # downd.start()
                    # downd2.start()
                    # requestFactoryProcess()
                    # downInUrlQueue.put(None)
                    # downd.join()
                    # downd2.join()


                else:
                    self.state = self.requestData.error(self.requestData)
                        
                # self.data = response.text;       
            else:
                print("retrydown:",self.requestData.url," retryTimes:",retryTimes);
                retryTimes-=1
                if retryTimes == 0:
                    self.state = False
                    print("download failed");
                    self.state = self.requestData.error(self.requestData)
                else:
                    self.downData(retryTimes=retryTimes,**kwargs)
        except (BaseException):
            print("retrydown:",self.requestData.url," retryTimes:",retryTimes);
            retryTimes-=1
            if retryTimes == 0:
                self.state = False
                print("download failed");
                self.state = self.requestData.error(self.requestData)
            else:
                self.downData(retryTimes=retryTimes,**kwargs)

            pass
        return self
    def getMethod(self):
        methods = self.requestData.methods.upper();
        if methods == "GET":
            return requests.get;
        elif methods=="POST":
            return requests.post;
        pass   

    def parseData(self):
        type = self.requestData.type.upper();
        if type == "BYTE":
            return self.getByte;
        if  type == "JSON":
            return self.getJson;
        elif type == "HTML":
            return self.getHtml;
    def getState(self):
        return self.state
    def getByte(self):
        return self.byteData
    def getHtml(self):
        return self.data
    def getJson(self):
        if self.data == None:
            return None
        else: 
            obj =  json.loads(self.data);
            return obj
