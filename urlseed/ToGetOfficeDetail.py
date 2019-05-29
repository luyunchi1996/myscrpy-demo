from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from  util.SqlCreate import SqlCreate;
from  entity.LawyerOffice import LawyerOffice;
from util.MySqlOperator import SimpleSqlOpeator;
from bs4 import BeautifulSoup;
class ToGetOfficeDetail(RequestData):
    def __init__(self,url="",id="",areaname=""):
        super(ToGetOfficeDetail).__init__()
        self.url =url
        self.id = id
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = None
        self.json = None;
        self.areaname = areaname
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        userInfo =soup.find(name="dl",attrs={"class":"user-info"})
        name = userInfo.find(name="dd",attrs={"class":"name"}).string
        name = str(name).replace("\n","").strip()
        keyMap ={}    
        infos = userInfo.find_all(name="dd",attrs={"class":"info"})
        for dd in infos:
            label = dd.contents[1].string
            label = str(label).replace("：","").strip()
            value = dd.contents[2]
            if isinstance(value,bs4.element.Tag):
                if str(value.name).__eq__("a"):
                    value = str(value["href"])
                else:
                    value = None
            else:
                value = str(value).replace("\n","").strip()
            keyMap[label]=value
        infoList =soup.find(name="ul",attrs={"class":"info-list"})
        infolis = infoList.find_all(name="li")
   
        for li in infolis:
            label = li.contents[0].string
            label = str(label).replace("：","").strip()
            value = li.contents[1].replace("\n","")
            value = value.strip()
            keyMap[label]=value   
        keyObj ={
            '执业证号': 'certNO', 
            '通讯地址': 'Address',  
            '联系电话': 'Tell',
        }
        lawyerOffice = LawyerOffice()
        urlList = []
        for key in keyObj:
            lawyerOffice.__setattr__(keyObj[key],keyMap[key])
        lawyerOffice.OfficeName = name
        lawyerOffice.OID = self.id
        lawyerOffice.CityCode = self.areaname
        print(keyMap)
        return {
            "datas":[lawyerOffice]
        }


    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        yield self


