from util.RequestData import RequestData;
import bs4;
from util.FileUtil import FileUtil;
from bs4 import BeautifulSoup;
from urlseed.ToGetUrl import ToGetUrl; 
class ToGetCompanyImportInfo(RequestData):

    def __init__(self):
        super(ToGetCompanyImportInfo).__init__()
        self.url ="https://www.hao123.com/"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = None;
        self.json = None;
    def success(self,data):
        soup = BeautifulSoup(data.data, "html.parser");
        ullist = soup.find_all(name="ul",attrs={"class","cls_bd"});
        togeturls = [] 
        for ul in ullist:
            lis = ul.find_all(name="li");
            for li in lis:
                a_list = li.find_all(name="a")
                for a in a_list:
                    title = a['data-title']
                    href = a['href'];
                    tgo = ToGetUrl(url=href,title=title)
                    togeturls.append(tgo)

            
            pass
        print(len(togeturls))
        return togeturls;

    def error(self,data):
        return True;
    def iserror(self,data):
        return True;
    def generate(self):
        yield self        


