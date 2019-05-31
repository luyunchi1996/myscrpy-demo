from util.RequestData import RequestData;
from util.FileUtil import FileUtil;

class ToGetByte(RequestData):
    def __init__(self,url="",fileName=""):
        super(ToGetByte).__init__()
        self.url =url
        self.fileName = fileName
        self.methods="GET"
        self.type="byte"
        self.queryString = None
        self.data=None;
        self.params = None;
        self.json = None;
        pass
    def success(self,data):
        FileUtil( filepath="./image/"+data.fileName,mode="wb",encoding=None).saveText(data.data)
        return True
    def error(self,data):
        return {
            "errorDatas": [data]
        };
    def iserror(self,data):
        return True
    def generate(self):
        yield self;