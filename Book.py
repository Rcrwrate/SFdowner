# from Lib.log import Log
from Lib.ini import CONF
import time


class BOOK():
    def __init__(self, name) -> None:
        self.c = CONF(name)
        self.l = []
        self.need = []
    # def check(self, data):
    #     '''True需要更新,False无需更新'''
    #     if data["status"]["httpCode"] == 403:
    #         self.forbidden.append(data["data"]["chapId"])
    #         return False
    #     T = self.c.load(data["data"]["chapId"])[0]
    #     if T:
    #         if self.time(data["data"]["updateTime"]) == T:
    #             return False
    #     self.need.append(data)
    #     return True

    def analysis(self, o):
        '''分析可下载章节'''
        for i in o["data"]["volumeList"]:
            for j in i["chapterList"]:
                if j["needFireMoney"] == 0:
                    self.l.append(j)
        return self.l

    def analysis_need(self):
        '''分析需要下载的章节'''
        for i in self.l:
            try:
                t = i["updateTime"]
            except:
                t = i["AddTime"]
            T = self.c.load(i["chapOrder"], i["chapId"])[0]
            if T:
                if self.time(t) != T:
                    self.need.append(i)
        return self.need

    def set_cache(self, o):
        '''设置'''
        for i in o:
            try:
                t = i["updateTime"]
            except:
                t = i["AddTime"]
            self.c.add(i["chapOrder"], i["chapId"], self.time(t))
        self.c.save()

    @staticmethod
    def time(t):
        t = time.strptime(t, "%Y-%m-%dT%H:%M:%S")
        t = time.mktime(t)
        return t


if __name__ == "__main__":
    b = BOOK("test")
    print(b.time("2018-11-16T23:26:16"))
