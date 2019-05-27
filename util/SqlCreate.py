from util.FileUtil import FileUtil;
from entity import *;
#读取配置数据

class Query():
    def __init_(self):
        self.queryList=[]
        self.entityJson={}
    def addQuery(self,filed,conditions,conditionsValue,autosubline):
        fi = filed
        if autosubline:
            fi = self.changeVariableName(filed)
        self.queryList.append(""+fi+" "+conditions+" '"+str(conditionsValue)+"'")
        return self
    def addAnd(self):
        self.queryList.append(" and ")
        return self
    def addOr(self):
        self.queryList.append(" or ")
        return self
    def getQuery(self):
        return "".join(self.queryList);
    def changeVariableName(self,listx):    
        listy = listx[0]
        for i in range(1,len(listx)):
            # listx[i] 直接copy 或 先加'_'再copy
            if listx[i].isupper() and not listx[i-1].isupper():# 加'_',当前为大写，前一个字母为小写
                listy+='_'
                listy+=listx[i]
            elif listx[i].isupper() and listx[i-1].isupper() and listx[i+1].islower():
                # 加'_',当前为大写，前一个字母为小写
                listy+='_'
                listy+=listx[i]
            else:
                listy+=listx[i]
        return listy.lower()
class SqlCreate(Query):
    def __init__(self,entitys,primaryKey="id",keyFilter=[],autoSubLine = True,tableName =""):
        super(SqlCreate, self).__init__()
        self.queryList =[];
        self.entitys = entitys;
        self.className = entitys.__class__.__name__
        self.primaryKey = primaryKey;
        self.primaryKeyData={};
        self.query="";
        self.sqlModel="";
        self.keyFilter=keyFilter;
        self.tableName =tableName
        self.objMap = {}
        self.autoSubLine = autoSubLine;
        for key,value in self.list_all_member(self.entitys):
             if primaryKey == key:
                self.primaryKeyData[primaryKey] =value
             else:
                lineText = key
                if self.autoSubLine:
                    lineText =  self.changeVariableName(key)
                self.objMap[lineText] = value;

        print("")
        # for key in self.entityJson:
        #     if primaryKey == key:
        #         self.primaryKeyData[primaryKey] =self.entitys.__getattribute__(key)
        #         continue 
        #     self.objMap[self.entityJson[key]] = self.entitys.__getattribute__(key);
        #     pass

        #self.id = self.entity.__getattribute__(primaryKey);
    def createInsert(self):
        self.sqlModel="Insert"
        return self
    def createSelect(self):
        self.sqlModel="Select"
        return self
    def createUpdate(self):
        self.sqlModel="Update"
        return self
    def getInsertSql(self):
        dbkey=[]
        dbvalue=[]
        for k in self.objMap:
            
            if self.objMap[k]!=None:
              dbkey.append(k)
              val=self.objMap[k]
              dbvalue.append("'"+str(val)+"'")

        
        INSERT_SQL = r"INSERT INTO "+self.tableName+" ("+self.primaryKey+","+",".join(dbkey)+") VALUES ('"+str(self.primaryKeyData[self.primaryKey])+"',"+",".join(dbvalue)+");"

        return INSERT_SQL;
    def getUpdateSql(self):
        dbKeyValue=[]
       
        for k in self.objMap:
            if self.objMap[k]!=None:
              dbKeyValue.append(k+"="+"'"+str(self.objMap[k])+"'")

        UPDATE_SQL = r"UPDATE "+self.tableName+" SET "+",".join(dbKeyValue)+"  WHERE "+self.getQuery()+";"
        return UPDATE_SQL
    def getSelectSql(self):
        que = self.getQuery();
        keys=[];
        keyStr=""
        if self.keyFilter.__len__() ==0:
           keyStr="*"
        else:
            for kf in self.keyFilter:
                k = kf
                if self.autoSubLine:
                    k = self.changeVariableName(kf)
                keys.append(k)

            keyStr=",".join(keys)
        if que=="":
            SELECT_SQL = r"SELECT "+keyStr+" FROM "+self.tableName +" "+que;
        else:
            SELECT_SQL = r"SELECT "+keyStr+" FROM "+self.tableName+" WHERE "+que+";"
        return SELECT_SQL
    def setQuery(self,query):
        return query;
    def addQuerys(self,filed,conditions,conditionsValue):
        return  self.addQuery(filed,conditions,conditionsValue,self.autoSubLine)
    def getSql(self):
        if self.sqlModel=="Insert":
           return self.getInsertSql();
        if self.sqlModel=="Select":
           return self.getSelectSql();
        if self.sqlModel=="Update":
           return self.getUpdateSql();             
    def changeVariableName(self,listx):    
        listy = listx[0]
        for i in range(1,len(listx)):
            # listx[i] 直接copy 或 先加'_'再copy
            if listx[i].isupper() and not listx[i-1].isupper():# 加'_',当前为大写，前一个字母为小写
                listy+='_'
                listy+=listx[i]
            elif listx[i].isupper() and listx[i-1].isupper() and listx[i+1].islower():
                # 加'_',当前为大写，前一个字母为小写
                listy+='_'
                listy+=listx[i]
            else:
                listy+=listx[i]
        return listy.lower()
    def list_all_member(self,entity):
        for name,value in vars(entity).items():
            yield (name,value);

