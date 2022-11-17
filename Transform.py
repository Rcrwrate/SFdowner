class Transform():
    @staticmethod
    def chaplist(l):
        fin = []
        for i in l:
            Uid = f'''{i["novelId"]}-{i["volumeId"]}-{i["chapId"]}'''
            fin.append({
                "Uid": Uid,
                "url": f"Text/{Uid}.xhtml",
                "title": i["title"]
            })
        return fin

    @staticmethod
    def analysis(dl):
        fin = []
        for i in dl:
            Uid = f'''{i["novelId"]}-{i["volumeId"]}-{i["chapId"]}'''
            text = {
                "Uid": Uid,
                "title": i["title"],
                "lines": []
            }
