import pymysql
#简单mysql数据库访问
class SimpleSqlOpeator:
    def __init__(self,ip="localhost",port=3306,user="root",pwd="123456",dbname=''):
        self.db = pymysql.connect(host=ip, user=user, passwd=pwd, database=dbname, port=port, db=None, charset="utf8")
        self.cursor = self.db.cursor()

    def executeSql(self,sql,method="select",result="more",autocommit=False):
        try:
            print(sql)
            self.execute(sql)
            if method == "select":
                if result == "one":
                    return self.fetchone()
                return  self.fetchall()
            # 提交到数据库执行
            if autocommit == True:
                self.commit()
            return "ok"
        except Exception as e:
            self.rollback()
            print("rollback")
            
    def execute(self,sql):
        self.cursor.execute(sql)
    def fetchone(self):
        return self.cursor.fetchone()
    def fetchall(self):
        return self.cursor.fetchall()
    def commit(self):
        self.db.commit()
    def rollback(self):
        self.db.rollback()
    def close(self):
        self.db.close()

