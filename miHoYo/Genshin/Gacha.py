##

import getpass
import requests
from urllib import parse
import json
from ..HoYoLAB.api import header
import time


def getDefaultLogPath():
    """log的默认路径"""
    user = getpass.getuser()
    # replace("原神","Genshin Impact") #global
    return f"C:\\Users\\{user}\\AppData\\LocalLow\\miHoYo\\原神\\output_log.txt"


def getGachaLogPage():
    """读取Log中的祈愿记录页面链接"""
    with open(getDefaultLogPath(), "r", encoding="utf-8") as log:
        for line in log.readlines():
            if line.startswith("OnGetWebViewPageFinish") and -1 != line.find("gacha"):
                return line[23:-1]
    raise Exception("getGachaLogPage : log中没有祈愿记录链接.")


def get_params(url: str):
    """获取链接中的参数"""
    p = parse.urlparse(url=url)
    qs = p.query.split("&")

    params = {}
    for q in qs:
        s = q.split("=")
        params[s[0]] = s[1]

    if "ext" in params:
        params["ext"] = json.loads(parse.unquote(params["ext"]))

    if "authkey" in params:
        params["authkey"] = parse.unquote(params["authkey"])

    return params


# def read_params_from_file():
#     with open("gacha_params.json", "r", encoding="utf-8") as file:
#         return json.load(file)


def write_params_to_file(params: dict):
    """查询参数写入本地"""
    with open("gacha_params.json", "w", encoding="utf-8") as file:
        json.dump(params, file, ensure_ascii=False, indent=4)


def getGachaLog(params, flag: bool = False):
    """flag 输出请求信息"""

    # 请求数据
    resp = requests.get(
        url="https://hk4e-api.mihoyo.com/event/gacha_info/api/getGachaLog",
        params=params,
        headers=header,
    )

    # 解析数据
    rb = json.loads(resp.content)
    if flag:
        print(
            f"page:{params['page']}  end_id:{params['end_id']}  code:{rb['retcode']}  msg:{rb['message']}"
        )

    # 服务器正常响应并处理
    if rb["retcode"] == 0:
        return rb["data"]

    # 服务器未正常处理请求
    print("getGachaLog : ", rb["message"])
    raise Exception("getGachaLog : request failed.")


def getGachaLogs(gacha_type: int, flag: bool = False):
    """flag 是否写入本地文件"""
    params = []
    try:
        # 读取查询参数
        params = get_params(url=getGachaLogPage())
        params["gacha_type"] = str(gacha_type)
        params["page"] = "1"
        params["size"] = "30"
        params["end_id"] = "0"
        write_params_to_file(params)

        # 查询
        all_data = []
        while True:
            ls = getGachaLog(params=params)["list"]
            
            # 查询结束
            if not len(ls):
                break
            
            # 合并数据
            all_data.extend(ls)
            params["end_id"] = ls[-1]["id"]
            params["page"] = str(int(params["page"]) + 1)

            time.sleep(0.2)

        # 存储源数据
        if flag:
            with open(params["gacha_type"] + ".json", "w", encoding="utf-8") as file:
                json.dump(all_data, fp=file, ensure_ascii=False, indent=4)

        return all_data
    except Exception as ex:
        # 异常处理
        print("getGachaLogs exception:", ex)
    return []
