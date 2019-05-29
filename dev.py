from util import RequestFactory
from util import DownLoad
import time
import urlseed.UrlSeedClzLoader;
classList = urlseed.UrlSeedClzLoader.getClassList()
requestFactory = RequestFactory(urlSeedList=classList);

def func(res,urlQueue):
    d = DownLoad(requestData=res);
    result = d.downData(headers={
        "user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"
    },timeout=2,verify=False);

    if  isinstance(result,list):
        subRequestFactory = RequestFactory(urlSeedList=result)
        for srf in subRequestFactory.requestInstance():
            urlQueue.append(srf)
    else:
        return True


def main():
    urlQueue = []
    waitFlag = []
    for rf in requestFactory.requestInstance():
        func(rf,urlQueue)
    while True:
        print("wait...")
        if len(urlQueue) == 0:
            if len(waitFlag)>=20:
                 break
            waitFlag.append(True)
            time.sleep(1)
            continue

        rd = urlQueue.pop()
        func(rd,urlQueue)
       
    print("end")
if __name__ == '__main__':
    main()