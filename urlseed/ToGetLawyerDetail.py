from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetOfficeDetail import  ToGetOfficeDetail;
from  util.SqlCreate import SqlCreate;
from  entity.Lawyer import Lawyer;
from util.MySqlOperator import SimpleSqlOpeator;

class ToGetLawyerDetail(RequestData):
    def __init__(self,url="",id="",areaname = "",imageUrl=""):
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
        self.imageUrl = imageUrl;
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser")
        multiItem = soup.find(name="div", attrs={"class": "multi-item"});
        infoList = soup.find(name="ul",attrs={"class": "info-list"});
        lis = infoList.find_all(name="li")
        sex = lis[0].contents[1]
        age = lis[1].contents[1]
        mingzu = lis[2].contents[1]
        zhenzhimianmao = lis[3].contents[1]
        xueli = lis[4].contents[1]
        zhiyeliebei = lis[6].contents[1]
        urllist = []

        datas = multiItem.find(name="div",attrs={"class":"data"});
        name = datas.find(name="h3").contents[0]
        nameType = datas.find(name="h3").contents[1].contents[0]
        dataInfos = datas.find_all(name="p",attrs={"class":"data-info"})
        certNo = dataInfos[0].contents[1]
        officeName =dataInfos[1].contents[1].contents[0]
        officeDetailUrl = dataInfos[1].contents[1]["href"]
        officeDetailID = officeDetailUrl.split("=")[1]
        urlPath  = "https://credit.justice.gov.cn/"+officeDetailUrl
        tgod = ToGetOfficeDetail(url=urlPath,id=officeDetailID,areaname=self.areaname)
        lawyer = Lawyer()
        lawyer.OID = self.id
        lawyer.Age = age;
        lawyer.CityCode = self.areaname
        lawyer.Education =  xueli
        lawyer.ImageUrl =self.imageUrl
        lawyer.LawOfficeOID = officeDetailID
        lawyer.LawyerType = zhiyeliebei
        lawyer.WorkCardNumber  = certNo
        lawyer.LawyerName= name
        sqFind = SqlCreate(entitys=lawyer,primaryKey="OID",keyFilter=["OID"],autoSubLine=False,tableName="t_lawyer").createSelect().addQuerys("OID","=",lawyer.OID).getSql()
        sso = SimpleSqlOpeator(ip="192.168.196.128",port=3306,user="root",pwd="123456",dbname="lawyer_scrapy")
        sqlresult =  sso.executeSql(sqFind,result="one")
        if sqlresult == None:
            sqInsert = SqlCreate(entitys=lawyer, primaryKey="OID", autoSubLine=False,tableName="t_lawyer").createInsert().getSql()
            sso.executeSql(sqInsert,method="Insert")
        sso.commit()
        sso.close()



        return [tgod]

    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        yield self


