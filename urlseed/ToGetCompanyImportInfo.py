from util.RequestData import RequestData;

class ToGetCompanyImportInfo(RequestData):

    def __init__(self):
        super(ToGetCompanyImportInfo).__init__()
        self.url ="http://www.baidu.com"
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.json = None;

    def success(self,data):
        
        pass
    def error(self,data):
        pass
    def iserror(self,data):
        return True;
    def generate(self):
        for i in range(0,1000):
            self.params ={
                "currentPage":i
            }
            yield self        


