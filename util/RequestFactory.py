
from util.RequestData import RequestData;

class RequestFactory(RequestData):
    def __init__(self,urlseed=None,urlSeedList =[]):
        self.urlseed = urlseed
        self.urlSeedList = urlSeedList
        super(RequestFactory).__init__()
    def setRequestData(self):
        if self.urlseed is not None:
            newObj = None;
            try:
                newObj = self.urlseed()
            except TypeError:
                newObj = self.urlseed
            for obj in newObj.generate():
                requestData = None
                try:
                    requestData = self.urlseed()
                except TypeError:
                    requestData = self.urlseed.__class__()        
                for key,value in self.list_all_member(obj):
                    requestData.__setattr__(key,value)
                yield requestData  
    def requestInstance(self):
        while len(self.urlSeedList) !=0:
            clz = self.urlSeedList.pop()
            self.urlseed= clz;
            for o in  self.setRequestData():
                 yield o; 
    def list_all_member(self,entity):
        for name,value in vars(entity).items():
            yield (name,value);
    
    
