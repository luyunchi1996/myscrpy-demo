from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetUrl import ToGetUrl; 
class ToGetLawyerInfo(RequestData):

    def __init__(self):
        super(ToGetLawyerInfo).__init__()
        self.url ="https://credit.justice.gov.cn/subjects.jsp?zoneId=All&typeId=10d341aea6674146b36dd23c25090f04&page=2"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = {
             "zoneId":"All",
             "typeId":"10d341aea6674146b36dd23c25090f04"
        };
        self.json = None;
    def success(self,data):
        soup = BeautifulSoup(data.data,"html.parser")
        multiItem= soup.find_all(name="a",attrs={"class":"multi-item"});
        for mi in multiItem:
            detailHref = mi['href']
            avatar =  mi.find(name="div",attrs={"class":"avatar"})["style"].split("(")
            datas = mi.find(name="div",attrs={"class":"data"})
            name = datas.find(name="h3").contents[0]
            nameType = datas.find(name="h3").contents[1].contents[0]
            dataInfos = datas.find_all(name="p",attrs={"class":"data-info"})

            certNo = dataInfos[0].contents[1]
            officeName =dataInfos[1].contents[1]
            print(detailHref,avatar,name,nameType)
            
        return True

    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        size = 33099//5+1 
        for page in range(1,size):
            self.params['page'] = page;
            yield self 


