from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetImage import ToGetByte;
from urlseed.ToGetLawyerDetail import ToGetLawyerDetail

class ToGetLawyerInfo(RequestData):

    def __init__(self,zoneid="All",areaname="",count=0):
        super(ToGetLawyerInfo).__init__()
        self.url ="https://credit.justice.gov.cn/subjects.jsp"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.areaName = areaname
        self.count = count
        self.params = {
             "zoneId":zoneid,
             "typeId":"10d341aea6674146b36dd23c25090f04"
        };
        self.json = None;
    def success(self,data):
        soup = BeautifulSoup(data.data,"html.parser")
        multiItem= soup.find_all(name="a",attrs={"class":"multi-item"});
        urlList = []
        for mi in multiItem:
            detailHref = mi['href']
            avatar =  mi.find(name="div",attrs={"class":"avatar"})["style"].split("(")[1].split(")")[0]
            # datas = mi.find(name="div",attrs={"class":"data"})

            id = detailHref.split("=")[1]
            # certNo = dataInfos[0].contents[1]
            # officeName =dataInfos[1].contents[1]
            filename = id+".png"
            tgb = ToGetByte(url=avatar,fileName=filename)
            urlPath  = "https://credit.justice.gov.cn/"+detailHref
            tgld=ToGetLawyerDetail(url=urlPath,id=id,areaname = data.areaName,imageUrl=filename)

            urlList.append(tgb)
            urlList.append(tgld)

        return urlList

    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        size = self.count//5+1
        for page in range(1,size):
            print("nowPage ",page)
            self.params['page'] = page;
            yield self 


