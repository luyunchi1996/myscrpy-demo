from util import RequestFactory
from util import DownLoad
import time
import urlseed.UrlSeedClzLoader;
classList = urlseed.UrlSeedClzLoader.getClassList()
requestFactory = RequestFactory(urlSeedList=classList);

def func(res,times=3):
    if times == 0:
        return
    d = DownLoad(requestData=res);
    result = d.downData(headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    },timeout=2);

    if  isinstance(result,list):
        subRequestFactory = RequestFactory(urlSeedList=result)
        for srf in subRequestFactory.requestInstance():   
            times-=1   
            func(srf,times)
    else:
        return True
def main():
    for rf in requestFactory.requestInstance():
        func(rf)
    print("end...")
if __name__ == '__main__':
    main()