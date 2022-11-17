from Lib.ini import CONF
from Lib.Network import Network
from Lib.log import Log
from Book import BOOK
import traceback


l = Log("SF", log_level=20)

URL = "https://minipapi.sfacg.com/"


class SFWX():
    def __init__(self) -> None:
        self.c = CONF("SF")
        self.s = Network({}, log_level=10)
        cookie = self.c.load("SF", "cookie")[0]
        self.changeHeader(cookie)

    def changeHeader(self, cookie):
        header = {"sf-minip-info": "minip_novel/1.0.70(android;11)/wxmp",
                  "Content-Type": "application/json"}
        if cookie != False:
            header["Cookie"] = cookie
        self.s.changeHeader(header, True)

    def login(self, username, password):
        date = {
            "username": username,
            "password": password
        }
        url = URL + "pas/mpapi/sessions"
        r = self.s.post(url, json=date)
        try:
            L = r.headers["Set-Cookie"].split(" ")
            i = 0
            while i < len(L):
                for j in ["expires", "domain", "path", "SameSite", "secure", "HttpOnly"]:
                    if j in L[i]:
                        del L[i]
                        i -= 1
                i += 1
            O = ""
            for i in L:
                if "=" in i:
                    O += i
            self.c.add("SF", "cookie", O)
            self.c.save()
            self.changeHeader(O)
            l.info("[SF][LOGIN][INFO]\t\tOK")
            print("[SF]INFO\t登录成功")
        except Exception:
            l.error(
                f"[SF][LOGIN][ERROR]\t\t{r}\t\t{r.text}\n{traceback.format_exc()}")
            print(f"[SF]ERROR\t登录失败\t{r.text}")

    def search(self, word):
        def state(state):
            if state:
                return "已完结"
            else:
                return "未完结"
        url = URL + \
            f"pas/mpapi/search/novels/result?q={word}&size=20&page=0&expand="
        r = self.s.get(url).json()
        print(f"关于{word}的搜索结果如下:\t")
        for i in r["data"]["novels"]:
            print("\tNoverID: {}\t《{}》{}著\t\t{}{}字".format(
                i["novelId"], i["novelName"], i["authorName"], state(i["isFinish"]), i["charCount"]))

    def info(self, noverID):
        url = URL + \
            f"pas/mpapi/novels/{noverID}?expand=latestchapter,chapterCount,typeName,intro,fav,ticket,pointCount,tags,sysTags,signlevel,discount,discountExpireDate,totalNeedFireMoney,originTotalNeedFireMoney"
        r = self.s.get(url).json()
        print("《{}》{}著".format(
            r["data"]["novelName"], r["data"]["authorName"]))
        print("上次更新:\n\t{}\n\t{}".format(
            r["data"]["expand"]["latestChapter"]["addTime"], r["data"]["expand"]["latestChapter"]["title"]))
        self.info = r

    def dir(self, noverID):
        url = URL + f"pas/mpapi/novels/{noverID}/dirs"
        r = self.s.get(url).json()
        print("卷列表:")
        for i in r["data"]["volumeList"]:
            print("\t"+i["title"])
        return r

    def chapter(self, chapId):
        url = URL + \
            f"pas/mpapi/Chaps/{chapId}?expand=content,needFireMoney,originNeedFireMoney,tsukkomi&autoOrder=true"
        r = self.s.get(url).json()
        return r

    def chapter_downloader(self, dl):

        def BASE_download(dl):
            print("开始下载,总计{}章".format(len(dl)))
            o = []
            err = []
            for i in dl:
                r = self.chapter(i["chapId"])
                if r["status"]["httpCode"] != 200:
                    print("[ERROR]:章节{}下载失败,将在稍后重试".format(i["title"]))
                    l.error("[SF][DOWNL][ERROR]\t\t{r}\t\t{r.text}\n")
                    err.append(i)
                else:
                    i["content"] = r["data"]["expand"]["content"]
                    o.append(i)
            return o, err

        o, err = BASE_download(dl)
        e = 0
        while len(err) != 0:
            tmp, err = BASE_download(err)
            o += tmp
            e += 1
            if e >= 5:
                break
        return o

    def download(self, noverID):
        self.info(noverID)
        self.b = BOOK(self.info["data"]["novelName"])
        dl = self.b.analysis_need(self.b.analysis(self.dir(noverID)))
        fin = self.chapter_downloader(dl)
        self.b.set_cache(fin)


API = "https://api.sfacg.com/"


class SF():
    def __init__(self) -> None:
        self.c = CONF("SF")
        self.s = Network({}, log_level=10)
        cookie = self.c.load("SF", "cookie")[0]
        self.changeHeader(cookie)

    def changeHeader(self, cookie):
        header = {
            "authorization": "Basic YW5kcm9pZHVzZXI6MWEjJDUxLXl0Njk7KkFjdkBxeHE=",
            "user-agent": "boluobao/4.6.36(android;23)/BDFZH2",
            "Content-Type": "application/json",
            'accept': 'application/vnd.sfacg.api+json;version=1',
            'sfsecurity': 'nonce=EE94F4D4-CC0B-43B6-BFF2-6CB72CE8698B&timestamp=1632459519271&devicetoken=F632BBEC-F075-39B5-A2C8-3234F5CBF99D&sign=7778A67648C9D95483E466D9D341FEA1',
        }
        if cookie != False:
            header["Cookie"] = cookie
        self.s.changeHeader(header, True)

    def login(self, username, password):
        date = {
            "username": username,
            "password": password
        }
        url = API + "sessions"
        r = self.s.post(url, json=date)
        try:
            L = r.headers["Set-Cookie"].split(" ")
            i = 0
            while i < len(L):
                for j in ["expires", "domain", "path", "SameSite", "secure", "HttpOnly"]:
                    if j in L[i]:
                        del L[i]
                        i -= 1
                i += 1
            O = ""
            for i in L:
                if "=" in i:
                    O += i
            self.c.add("SF", "cookie", O)
            self.c.save()
            self.changeHeader(O)
            l.info("[SF][LOGIN][INFO]\t\tOK")
            print("[SF]INFO\t登录成功")
        except Exception:
            l.error(
                f"[SF][LOGIN][ERROR]\t\t{r}\t\t{r.text}\n{traceback.format_exc()}")
            print(f"[SF]ERROR\t登录失败\t{r.text}")

    def search(self, word):
        def state(state):
            if state:
                return "已完结"
            else:
                return "未完结"
        url = API + \
            f"pas/mpapi/search/novels/result?q={word}&size=20&page=0&expand="
        r = self.s.get(url).json()
        print(f"关于{word}的搜索结果如下:\t")
        for i in r["data"]["novels"]:
            print("\tNoverID: {}\t《{}》{}著\t\t{}{}字".format(
                i["novelId"], i["novelName"], i["authorName"], state(i["isFinish"]), i["charCount"]))

    def info(self, noverID):
        url = API + \
            f"novels/{noverID}?expand=latestchapter,chapterCount,typeName,intro,fav,ticket,pointCount,tags,sysTags,signlevel,discount,discountExpireDate,totalNeedFireMoney,originTotalNeedFireMoney"
        r = self.s.get(url).json()
        print("《{}》{}著".format(
            r["data"]["novelName"], r["data"]["authorName"]))
        print("上次更新:\n\t{}\n\t{}".format(
            r["data"]["expand"]["latestChapter"]["addTime"], r["data"]["expand"]["latestChapter"]["title"]))
        self.info = r

    def dir(self, noverID):
        url = API + f"novels/{noverID}/dirs"
        r = self.s.get(url).json()
        print("卷列表:")
        for i in r["data"]["volumeList"]:
            print("\t"+i["title"])
        return r

    def chapter(self, chapId):
        url = API + \
            f"Chaps/{chapId}?expand=content,needFireMoney,originNeedFireMoney,tsukkomi&autoOrder=true"
        r = self.s.get(url).json()
        return r

    def chapter_downloader(self, dl):

        def BASE_download(dl):
            print("开始下载,总计{}章".format(len(dl)))
            o = []
            err = []
            for i in dl:
                r = self.chapter(i["chapId"])
                if r["status"]["httpCode"] != 200:
                    print("[ERROR]:章节{}下载失败,将在稍后重试".format(i["title"]))
                    l.error("[SF][DOWNL][ERROR]\t\t{r}\t\t{r.text}\n")
                    err.append(i)
                else:
                    i["content"] = r["data"]["expand"]["content"]
                    o.append(i)
            return o, err

        o, err = BASE_download(dl)
        e = 0
        while len(err) != 0:
            tmp, err = BASE_download(err)
            o += tmp
            e += 1
            if e >= 5:
                break
        return o

    def download(self, noverID):
        self.info(noverID)
        self.b = BOOK(self.info["data"]["novelName"])
        dl = self.b.analysis_need(self.b.analysis(self.dir(noverID)))
        fin = self.chapter_downloader(dl)
        self.b.set_cache(fin)

    def signin(self):
        url = API + "user/signInfo"
        self.s.put(url, data="")

    def me(self):
        url = API + "user"
        self.s.get(url)


if __name__ == "__main__":
    # s = SFWX()
    # # s.download("466073")
    # s.info("466073")
    # b = BOOK(s.info["data"]["novelName"])
    # b.analysis(s.dir("466073"))
    # fin = s.chapter_downloader(b.l)
    # for i in fin:
    #     print(i["content"])
    # # from Transform import Transform
    # # print(Transform.chaplist(b.l))
    s = SF()
    # s.chapter("5795793")
    
    s.me()
