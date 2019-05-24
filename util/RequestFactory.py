
from util.RequestData import RequestData;
import urlseed.UrlSeedClzLoader;

classList = urlseed.UrlSeedClzLoader.getClassList()
class RequestFactory(RequestData):
    def __init__(self):
        super(RequestFactory).__init__()
    def requestInstance(self):
        while len(classList) !=0:
            clz = classList.pop()
            obj = clz();
            for obj in obj.generate():
                requestData = clz()
                for key,value in self.list_all_member(obj):
                    requestData.__setattr__(key,value)
                yield requestData
        print("finish")    
    def list_all_member(self,entity):
        for name,value in vars(entity).items():
            yield (name,value);
    
    
