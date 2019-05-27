from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.GetPageSize import GetPageSize
class GetLawyerInArea(RequestData):
    def __init__(self):
        super(RequestData).__init__()
        self.url ="https://credit.justice.gov.cn/subjects.jsp"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = None
        self.json = None;
        pass
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        filterList = soup.find_all(name="ul",attrs={"class":"filter-list"})
        areaInfo = filterList[1].find_all(name="a")
        urllist = []
        for li in areaInfo:

            if li.contents[0].__eq__("全部"):
                continue
            href = li["href"].split(",")[1].split(");")[0]
            zoneId = str(href.replace("'","").strip())
            areaname = str(li.contents[0])
            gpz = GetPageSize(zoneid=zoneId,areaName=areaname)
            urllist.append(gpz)
        return urllist
    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        yield self
