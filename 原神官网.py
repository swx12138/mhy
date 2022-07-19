# ?pageSize=5&pageNum=12&channelId=10

from os import chdir, mkdir
from os.path import exists

import wget
from bs4 import BeautifulSoup
from kokomi.miHoYo.HoYoLAB import api


def GetAllNews():
    param = {"pageSize": 30, "pageNum": 1, "channelId": 10}
    data = api.getContentListMi(params=param)
    return data


def getImgLink(contentId: int):
    resp = api.getContent({"contentId": contentId, "around": 1})
    bs = BeautifulSoup(resp["content"], features="lxml")
    return bs.find("img").attrs["src"]


if __name__ == "__main__":
    chdir("img")
    if not exists("birth"):
        mkdir("birth")
    chdir("birth")

    data = GetAllNews()
    for item in data["list"]:
        try:
            if "生日快乐" in item["title"]:
                u = getImgLink(item["contentId"])
                wget.download(u)
        except Exception as e:
            print(e)
