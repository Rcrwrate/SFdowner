# from Lib.log import Log
from Lib.ini import CONF
import time


class BOOK():
    def __init__(self, name) -> None:
        self.c = CONF(name)
        self.l = []  # 文章顺序
        self.need = []

    def analysis(self, o):
        '''分析可下载章节'''
        for i in o["data"]["volumeList"]:
            for j in i["chapterList"]:
                if j["needFireMoney"] == 0:
                    j["title"] = i["title"] + "  " + j["title"]
                    self.l.append(j)
        return self.l

    def analysis_need(self, o):
        '''分析需要下载的章节'''
        for i in o:
            if i["updateTime"] != None:
                t = i["updateTime"]
            else:
                t = i["AddTime"]
            T = self.c.load(str(i["volumeId"]), str(i["chapId"]))[0]
            if T != False:
                if self.time(t) == T:
                    continue
            self.need.append(i)
        return self.need

    def set_cache(self, o):
        '''设置'''
        for i in o:
            if i["updateTime"] != None:
                t = i["updateTime"]
            else:
                t = i["AddTime"]
            self.c.add(str(i["volumeId"]), str(i["chapId"]), self.time(t))
        self.c.save()

    @staticmethod
    def time(t):
        t = time.strptime(t, "%Y-%m-%dT%H:%M:%S")
        t = time.mktime(t)
        return str(t)


if __name__ == "__main__":
    b = BOOK("test")
    print(b.time("2018-11-16T23:26:16"))
