from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetLawyerInfo import ToGetLawyerInfo
class GetPageSize(RequestData):
    def __init__(self,zoneid="All",areaName=""):
        super(RequestData).__init__()
        self.url ="https://credit.justice.gov.cn/subjects.jsp"
        self.methods="GET"

        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = {
            "zoneId": zoneid,
            "typeId": "10d341aea6674146b36dd23c25090f04"
        };
        self.areaName = areaName
        self.json = None;

        pass
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        listcount = soup.find(name="div",attrs={"class":"list-count"}).string
        listcount = listcount.split("共")[1].replace("条","").strip()
        count = int(listcount)
        zoneid = self.params["zoneId"]
        glf = ToGetLawyerInfo(zoneid=zoneid,areaname=self.areaName,count=count)
        return  [glf]


    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        yield self
