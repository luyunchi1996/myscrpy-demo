import json
import os
from shutil import copy


class FileUtil:
    def __init__(self,filepath="",mode="r",encoding="utf-8"):
        self.filepath=filepath
        self.mode = mode
        self.encoding = encoding
    def readJson(self):
        with open(self.filepath, mode=self.mode, encoding=self.encoding) as f:
            data = json.load(f)
        return data
    def saveJson(self,data):
        with open(self.filepath, mode=self.mode, encoding=self.encoding) as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    def listfile(self):
        filelist = os.listdir(self.filepath)
        for file in filelist:
            if not os.path.isfile(self.filepath+"/"+file):
                filelist.remove(file)
        return filelist
    def saveFile(self,data=[]):
        if type(data) != type([]): return None
        fp = open(self.filepath, mode=self.mode, encoding=self.encoding)
        for ls in data:
            fp.write(str(ls)+"\n")
        fp.close()
        return "Success"
    def saveText(self,text=""):
        with open(self.filepath, mode=self.mode, encoding=self.encoding) as f:
            f.write(text)
            
    def readText(self):
        with open(self.filepath, mode=self.mode, encoding=self.encoding) as f:
            text =f.read()
        return text
    def readFile(self):
        fp = open(self.filepath, mode=self.mode, encoding=self.encoding)
        list =[]
        for ls in fp:
            if ls =="\n":continue
            list.append(ls.replace("\n",""))
        fp.close()
        return list
    def findFile(self,name):
        dirlist = os.listdir(self.filepath)
        for dirs in dirlist:
            if os.path.isdir(self.filepath + "/" + dirs):
                if os.path.exists(self.filepath + "/" + dirs + "/" + name):
                    return self.filepath + "/" + dirs + "/" + name
        return None
    def moveFile(self,oriPath,tarPath):
        copy(oriPath,tarPath)
        os.remove(oriPath)
        return True
    def makedir(self):
        if  not os.path.exists(self.filepath):
            os.mkdir(self.filepath)
    def saveDict(self,dict={}):
        if type(dict) != type({}): return None
        fp = open(self.filepath, mode=self.mode, encoding=self.encoding)
        for key in dict:
            fp.write(key+":"+str(dict[key])+"\n")
        fp.close()
    def readDict(self):
        fp = open(self.filepath, mode=self.mode, encoding=self.encoding)
        dict ={}
        for ls in fp:
            if ls == "\n": continue
            strs =ls.replace("\n", "").split(":",1)
            dict[strs[0]] = strs[1]
        fp.close()
        return dict
    def isExists(self):
        return os.path.exists(self.filepath)


