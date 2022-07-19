##

import json
from os import chdir, mkdir

import matplotlib.pyplot as plt
from genericpath import exists
from kokomi.miHoYo.Genshin.GetGacha import GachaException, getGachaLogs
from pandas import DataFrame, ExcelWriter
from tabulate import tabulate

characters = [
    "迪卢克",
    "琴",
    "莫娜",
    "七七",
    "刻晴",
    "温迪",
    "可莉",
    "达达利亚",
    "钟离",
    "阿贝多",
    "甘雨",
    "魈",
    "胡桃",
    "优菈",
    "万叶",
    "霄宫",
    "神里绫华",
    "雷电将军",
    "珊瑚宫心海",
    "荒泷一斗",
    "申鹤",
    "神里凌人",
    "夜兰",
]

gacha_pools = {
    301: "角色限定祈愿",
    302: "神铸赋形",
    200: "奔行世间",
    100: "新手祈愿",
}


def read_loacl_json(id):
    """读取本地json并转为DataFrame"""
    all_data = readGachaLogsNb(id)
    all_data.reverse()

    times_count = 0
    low_count = 0
    baeuty_data = []
    for data in all_data:
        times_count += 1
        low_count += 1
        baeuty_data.append(
            {
                "时间": data["time"],
                "名称": data["name"],
                "类别": data["item_type"],
                "星级": data["rank_type"],
                "总次数": times_count,
                "保底内": low_count,
            }
        )
        if data["rank_type"] == "5":
            low_count = 0

    return DataFrame(baeuty_data)


def readGachaLogs(gacha_type: int):
    """读取本地抽卡记录"""
    with open(str(gacha_type) + ".json", "r", encoding="utf-8") as file:
        return json.load(fp=file)


def readGachaLogsNb(gacha_type: int) -> list:
    """读取本地抽卡记录"""
    with open(str(gacha_type) + "_nb.json", "r", encoding="utf-8") as file:
        return json.load(fp=file)


def getEndId(gacha_type: int):
    with open(str(gacha_type) + "_nb.json", "r", encoding="utf-8") as file:
        return json.load(fp=file)[0]["id"]


class GachaLogEmptyList(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


def updateNb(gacha_type: int):
    """从祈愿记录页更新本地数据"""

    print("updating  ", gacha_pools[gacha_type], f"  {getEndId(gacha_type)}")

    all_data = getGachaLogs(gacha_type)
    if not all_data:
        # continue
        raise GachaLogEmptyList

    old_data = readGachaLogsNb(gacha_type)

    with open(str(gacha_type) + "_nb.json", "w", encoding="utf-8") as file:
        json.dump(
            obj=all_data + old_data[len(all_data) - all_data.index(old_data[0]) :],
            fp=file,
            ensure_ascii=False,
            indent=4,
        )


def updateNbs():
    """从祈愿记录页更新本地数据"""

    for ty in [("武器", 302), ("角色", 301), ("常驻", 200), ("新手", 100)]:
        try:
            updateNb(gacha_type=ty[1])
        except GachaLogEmptyList:
            continue
    print("update all done.")


# TODO:rebuild
def See_LocalData(all_local: dict):
    """可视化"""

    # 支持中文
    plt.rcParams["font.sans-serif"] = ["SimHei"]  # 用来正常显示中文标签
    plt.rcParams["axes.unicode_minus"] = False  # 用来正常显示负号

    # 每个池子统计
    index = 1
    for pname in all_local:
        # 四星五星数量
        count = {
            "five": 0,
            "four": 0,
            "all": len(all_local[pname]),
        }

        for data in all_local[pname]:
            if data["rank_type"] == "5":
                count["five"] += 1
            elif data["rank_type"] == "4":
                count["four"] += 1

        plt.subplot(2, 2, index)

        plt.pie(
            x=[
                count["five"],
                count["four"],
            ],
            labels=["五星", "四星"],
            colors=["yellow", "purple"],
        )

        index += 1
    plt.title("统计")
    plt.show()


def Read_Local_Data():
    """读取所有本地记录"""
    all_data = {}
    for pool_id in gacha_pools:
        try:
            pool_data = readGachaLogsNb(pool_id)
            pool_data.reverse()
            all_data[gacha_pools[pool_id]] = pool_data
        except GachaException as g:
            print(g.what())
    return all_data


def Count_Five(local_data):
    """统计五星数量"""
    all_five = {}
    for pname in local_data:
        try:
            all_five[pname] = []
            gacha_times = 0
            pool_data = local_data[pname]
            for data in pool_data:
                gacha_times += 1
                if data["rank_type"] == "5":
                    all_five[pname].append({"name": data["name"], "times": gacha_times})
                    gacha_times = 0
        except GachaException as g:
            print(g.what())
    return all_five


def PandasDF_PrintConsole(all_five: dict, export: bool = False):
    """输出五星统计表格到控制台"""
    all_ff = {}
    max_len = max([len(five) for five in all_five.values()])  # 5星最多的池子里5星数量
    for five in all_five:
        fives = all_five[five]
        all_ff[five] = [f"{f['name']}[{f['times']}]" for f in fives]
        all_ff[five].extend([None] * (max_len - len(all_ff[five])))

    # 控制台输出
    # pandas.set_option('display.unicode.ambiguous_as_wide', True)
    # pandas.set_option('display.unicode.east_asian_width', True)
    # pandas.set_option('display.width', 360)
    df = DataFrame(all_ff)
    print(tabulate(df, headers=df.head(0), tablefmt="fancy_grid"))

    # 导出excel
    if export:
        with ExcelWriter(f"export.xlsx") as writer:
            for five in all_five:
                DataFrame(all_five[five]).to_excel(
                    writer,
                    sheet_name=five,
                    index=False,
                    encoding="utf-8",
                )


def main():
    # 更新本地记录
    updateNbs()

    # 读取本地记录
    all_data = Read_Local_Data()

    # 统计5星
    all_five = Count_Five(all_data)

    # 控制台输出5星统计表格
    #   - 可选：输出到excel
    PandasDF_PrintConsole(all_five)

    # See_LocalData(all_data)


if __name__ == "__main__":
    HOME_PATH = "GachaData"
    if not exists(HOME_PATH):
        mkdir(HOME_PATH)
    chdir(HOME_PATH)

    main()
