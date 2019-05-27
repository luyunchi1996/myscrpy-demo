from util.RequestData import RequestData;
from util.FileUtil import FileUtil;
class ToGetUrl(RequestData):
    def __init__(self,url="",title=""):
        super(ToGetUrl).__init__()
        self.url =url
        self.methods="GET"
        self.type="html"
        self.queryString = None
        self.data=None;
        self.params = None;
        self.json = None;
        self.title = title;
        pass
    def success(self,data):
        FileUtil( filepath="./test/"+data.title+".html",mode="w").saveText(data.data)

        return True
    def error(self,data):
        pass
    def iserror(self,data):
        return True
    def generate(self):
        yield self;