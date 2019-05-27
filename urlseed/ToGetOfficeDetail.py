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
        multiItem = soup.find(name="div", attrs={"class": "multi-item"});
        infoList = soup.find(name="ul", attrs={"class": "info-list"});
        lis = infoList.find_all(name="li")

        dizhi = lis[1].contents[1]
        tongyicode = lis[5].contents[1]
        cuanzen = lis[9].contents[1]
        lianxitel = lis[10].contents[1]

        datas = multiItem.find(name="div", attrs={"class": "data"});
        name = datas.find(name="h3").contents[0]

        dataInfos = datas.find_all(name="p", attrs={"class": "data-info"})
        certNo = dataInfos[0].contents[1]
        lawyerOffice = LawyerOffice()
        lawyerOffice.OID = self.id
        lawyerOffice.OfficeName =name
        lawyerOffice.Address = dizhi
        lawyerOffice.CityCode = self.areaname
        lawyerOffice.Tell = lianxitel
        lawyerOffice.certNO = certNo
        lawyerOffice.socialCode = tongyicode
        sqFind = SqlCreate(entitys=lawyerOffice, primaryKey="OID", keyFilter=["OID"], autoSubLine=False,
                           tableName="t_lawoffice").createSelect().addQuerys("OID", "=", lawyerOffice.OID).getSql()
        sso = SimpleSqlOpeator(ip="192.168.196.128", port=3306, user="root", pwd="123456", dbname="lawyer_scrapy")
        sqlresult = sso.executeSql(sqFind, result="one")
        if sqlresult == None:
            sqInsert = SqlCreate(entitys=lawyerOffice, primaryKey="OID", autoSubLine=False,tableName="t_lawoffice").createInsert().getSql()
            sso.executeSql(sqInsert,method="Insert")
        sso.commit()
        sso.close()
        return True

    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        yield self


