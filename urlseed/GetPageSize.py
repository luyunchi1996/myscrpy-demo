from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetLawyerInfo import ToGetLawyerInfo
class GetPageSize(RequestData):
    def __init__(self,zoneid="All",areaName=""):
        super(RequestData).__init__()
        self.url ="http://credit.lawyers.org.cn/lawyer-list.jsp"
        self.methods="GET"

        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = {
            "zoneCode": zoneid,
        };
        self.areaName = areaName
        self.json = None;
        self.zoneId = zoneid
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        h4 = soup.find(name="h4",attrs={"class":"list-title"})
        title = str(h4.string)
        count = title.split(" ")[1]
        # listcount = soup.find(name="div",attrs={"class":"list-count"}).string
        # listcount = listcount.split("共")[1].replace("条","").strip()
        # count = int(listcount)
        # zoneid = self.params["zoneId"]
        urlList = []
        for  i in range(1,int(count)):
            glf = ToGetLawyerInfo(zoneid=self.zoneId,areaname=self.areaName,count=int(count))
            glf.params["page"] = i
            urlList.append(glf)
        return urlList


    def error(self,data):
        return {
            "errorDatas": [data]
        };
    def iserror(self,data):
        return True;
    def generate(self):
        yield self
