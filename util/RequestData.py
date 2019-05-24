class RequestData:

    def __init__(self):
        self.id="";
        self.taskName="";
        self.url = None;
        self.methods = None;
        self.params = None;
        self.data=None;
        self.queryString=None;
        self.json = None;
        self.type = None;
    def success(self,data):
        pass
    def error(self,data):
        pass
    def iserror(self,data):
        pass
    def generate(self):
        
        pass

    
 