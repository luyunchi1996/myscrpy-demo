from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetOfficeDetail import  ToGetOfficeDetail;
from  util.SqlCreate import SqlCreate;
from  entity.Lawyer import Lawyer;
from util.MySqlOperator import SimpleSqlOpeator;
from urlseed.ToGetImage import ToGetByte;


class ToGetLawyerDetail(RequestData):
    def __init__(self,url="http://credit.lawyers.org.cn/lawyer.jsp?id=1dd45a7e1a574af2b18efdfb883398e8",id="1dd45a7e1a574af2b18efdfb883398e8",areaname = "黄浦"):
        super(ToGetLawyerDetail).__init__()
        self.url =url
        self.id = id
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = None
        self.json = None;
        self.areaname= areaname;
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        userInfo =soup.find(name="dl",attrs={"class":"user-info"})

        avtar = userInfo.find(name="dt",attrs={"class":"avatar"})
        avtarimg = avtar.find(name="img")['src']
        avtarimg = str(avtarimg).split("?")[0]
        name = userInfo.find(name="dd",attrs={"class":"name"}).string
        name = str(name).replace("\n","").strip()
        keyMap ={}    
        infos = userInfo.find_all(name="dd",attrs={"class":"info"})
        officeName = ""
        for dd in infos:
            label = dd.contents[0].string
            label = str(label).replace("：","").strip()
            value = dd.contents[1]
            if isinstance(value,bs4.element.Tag):
                if str(value.name).__eq__("a"):
                    officeName = str(value.string)
                    value = str(value["href"])
                     
                else:
                    value = None
            else:
                value = str(value).replace("\n","").strip()
            keyMap[label]=value
        
   

        infoList =soup.find(name="ul",attrs={"class":"info-list"})
        infolis = infoList.find_all(name="li")
   
        for li in infolis:
            if len(li.contents) == 1:
                label = li.contents[0].string
                label = str(label).replace("：","").strip()
                keyMap[label]=""
            elif len(li.contents) > 1:
                label = li.contents[0].string
                label = str(label).replace("：","").strip()
                value = li.contents[1].replace("\n","")
                value = value.strip()
                keyMap[label]=value

   
        keyObj ={
            '执业证号': 'WorkCardNumber', 
            '执业机构': 'LawOfficeOID', 
            '性别': 'Sex', 
            '年龄': 'Age', 
            '学历': 'Education', 
            '执业类型': 'LawyerType',
        }
        lawyer  = Lawyer()
        urlList = []
        for key in keyObj:
            lawyer.__setattr__(keyObj[key],keyMap[key])
        lawyerofficehref = lawyer.LawOfficeOID;
        oid =  lawyerofficehref.split("=")[1]
        lawyer.LawOfficeOID = oid;
        lawyer.OfficeName = officeName;
        lawyer.OID = self.id;
        url ="http://credit.lawyers.org.cn/"+lawyerofficehref
        toGetOfficeDetail = ToGetOfficeDetail(url=url,id=lawyer.LawOfficeOID,areaname=self.areaname)
        lawyer.LawyerName = name
        lawyer.CityCode = self.areaname
        lawyer.ImageUrl = lawyer.OID+".png"
        urlList.append(toGetOfficeDetail)
        
        toGetByte = ToGetByte(url=avtarimg,fileName=lawyer.OID+".png")
        urlList.append(toGetByte)
        
        return {
            "datas":[lawyer],
            "urlList":urlList
        }

    def error(self,data):
        return {
            "errorDatas": [data]
        };
    def iserror(self,data):
        return True;
    def generate(self):
        yield self


