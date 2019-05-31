from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.GetPageSize import GetPageSize
class GetLawyerInArea(RequestData):
    def __init__(self):
        super(RequestData).__init__()
        self.url ="http://credit.lawyers.org.cn/lawyer-list.jsp"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = None
        self.json = None;
        pass
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        # FileUtil(filepath="./image/demo.html",mode="w").saveText(data.data)
        filterList = soup.find_all(name="ul",attrs={"class":"filter-options"})
        areaInfo = filterList[0].find_all(name="a")
        urllist = []
        for a in areaInfo:
            textname = str(a.string).replace("\n","").strip();
            if textname.__eq__("全部"):
                continue
            zoneId = a["href"].split("'")[1].strip()
            gpz = GetPageSize(zoneid=zoneId,areaName=textname)
            urllist.append(gpz)
        return urllist
    def error(self,data):
        return {
            "errorDatas":[data]
        };
    def iserror(self,data):
        return True;
    def generate(self):
        yield self
