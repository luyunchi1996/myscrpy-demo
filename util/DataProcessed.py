
from util.DataProcess import DataProcess
import config
class DataProcessed:
    def __init__(self,ori,tar):
        self.ori = ori
        self.tar = tar
        # 提取dataProcess
        self.dataProcessDict ={}
        self.funcDict ={}
        self.tempTarDict ={}
        for k,v in self.list_all_member(tar):
            if isinstance(v,DataProcess):
                self.dataProcessDict[k] = v
                tar.__setattr__(k,"")   
                pass
            elif isinstance(v,str):
                pass
        pass
    def saveValue(self):
        # 读取 dataProcessDict 和 ori 的值
        for key in self.dataProcessDict:
            dpd = self.dataProcessDict[key]
        
            self.tempTarDict[key]=""
            value = self.ori.__getattribute__(dpd.filedName)
            if isinstance(value,list):
                count = 0;
                for o in value:
                    if o:
                       count+=1
                if count == 0:
                    value =""
            if dpd.processFun in self.funcDict:
               processFunc  = self.funcDict[dpd.processFun]

               self.tempTarDict[key] =  processFunc(params=(dpd.params,value))
            else:
                self.tempTarDict[key] =value
                continue  
            pass
        # 合并 tempTarDict 和 tar 的值
        for k,v in self.list_all_member(self.tar):
            value=""
            if k in self.ori.__dir__():
                value = self.ori.__getattribute__(k)
            if isinstance(v,list):
                count = 0;
                for o in v:
                    if o:
                       count+=1
                if count == 0:
                    value =""
            self.tar.__setattr__(k,value)
            if k in  self.tempTarDict:
                value = self.tempTarDict[k]
                self.tar.__setattr__(k,value)
           
    def getValue(self):
        return self.tar
    def list_all_member(self,entity):
        for name, value in vars(entity).items():
            yield (name, value);
    def setFuncDict(self,funcDict):
        self.funcDict = funcDict