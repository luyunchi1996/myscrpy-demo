from lib.RequestData import RequestData
from lib.RequestFactory import testdemo
@testdemo
class ToGetCompanyImportInfo(RequestData):

    def __init__(self):
        super(ToGetCompanyImportInfo).__init__()
        print("init")
    def success(self):
        pass
    def error(self):
        pass
    def iserror(self):
        pass
    def generateRole(self):
        pass


