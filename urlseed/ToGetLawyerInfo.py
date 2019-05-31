from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;

from urlseed.ToGetLawyerDetail import ToGetLawyerDetail

class ToGetLawyerInfo(RequestData):
    def __init__(self, zoneid="All", areaname="", count=0):
        super(ToGetLawyerInfo).__init__()
        self.url ="http://credit.lawyers.org.cn/lawyer-list.jsp"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.areaName = areaname
        self.count = count
        self.params = {
            "zoneCode":zoneid,
            "page":1
        };
        self.json = None;
    def success(self,data):
        soup = BeautifulSoup(data.data,"html.parser")
        # list-item
        listItem = soup.find_all(name="a",attrs={"class":"list-item"});
        urlList = []

        for li in listItem:
            href = li['href']
            id = href.split("=")[1]
            url="http://credit.lawyers.org.cn/"+href
            tgld=ToGetLawyerDetail(url=url,id=id,areaname = data.areaName)
            urlList.append(tgld)

        return urlList


    def error(self,data):
        return {
            "errorDatas": [data]
        };
    def iserror(self,data):
        return True;
    def generate(self):
        yield self 


