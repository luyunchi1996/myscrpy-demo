
from util.RequestData import RequestData;
import urlseed.UrlSeedClzLoader;

classList = urlseed.UrlSeedClzLoader.getClassList()
class RequestFactory(RequestData):
    def __init__(self,urlseed=None):
        self.urlseed = urlseed
        super(RequestFactory).__init__()
    def setRequestData(self):
        if self.urlseed is not None:
            newObj = self.urlseed()
            for obj in newObj.generate():
                requestData = self.urlseed()
                for key,value in self.list_all_member(obj):
                    requestData.__setattr__(key,value)
                yield requestData  
    def requestInstance(self):
        
        while len(classList) !=0:
            clz = classList.pop()
            self.urlseed= clz;
            for o in  self.setRequestData():
                 yield o;
        print("finish")    
    def list_all_member(self,entity):
        for name,value in vars(entity).items():
            yield (name,value);
    
    
