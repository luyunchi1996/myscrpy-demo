from util.RequestData import RequestData
class ToGetCompanyImportInfo(RequestData):

    def __init__(self):
        super(ToGetCompanyImportInfo).__init__()
        self.url ="http://www.baidu.com"
        self.methods="GET"    
    def success(self):
        pass
    def error(self):
        pass
    def iserror(self):
        pass
    def generate(self):
        for i in range(0,10):
            self.params ={
                "currentPage":i
            }
            yield self        


