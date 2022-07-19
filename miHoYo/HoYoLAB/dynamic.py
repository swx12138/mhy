# encode utf-8

import json

import requests

header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.55",
    "Referer": "https://bbs.mihoyo.com/",
}


def GetPostFull(post_id: int):
    api = "https://bbs-api.mihoyo.com/post/wapi/getPostFull"
    param = {"gids": "2", "post_id": str(post_id), "read": "1"}
    r = requests.get(api, params=param, headers=header)
    r.encoding = "gb2312"
    j = json.loads(r.content)
    return j["data"]
