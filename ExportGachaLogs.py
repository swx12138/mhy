##

import json
from os import chdir, mkdir

import matplotlib.pyplot as plt
from genericpath import exists
from pandas import DataFrame, ExcelWriter
from tabulate import tabulate

from miHoYo.Genshin.Gacha import getGachaLogs

gacha_pools = {
    301: "角色限定祈愿",
    302: "神铸赋形",
    200: "奔行世间",
    100: "新手祈愿",
}


def Read_GachaLogs(gacha_type: int):
    """[deprecated]读取本地抽卡记录"""
    with open(str(gacha_type) + ".json", "r", encoding="utf-8") as file:
        return json.load(fp=file)


def Read_GachaLogs_NewBetter(gacha_type: int) -> list:
    """读取本地抽卡记录"""
    with open(str(gacha_type) + "_nb.json", "r", encoding="utf-8") as file:
        return json.load(fp=file)


def Get_EndId(gacha_type: int):
    with open(str(gacha_type) + "_nb.json", "r", encoding="utf-8") as file:
        return json.load(fp=file)[0]["id"]


# class GachaLogEmptyList(Exception):
#     def __init__(self, *args: object) -> None:
#         super().__init__(*args)


def Update_NewBetter(gacha_type: int):
    """从祈愿记录页更新本地数据"""

    print("updating  ", gacha_pools[gacha_type], f"  {Get_EndId(gacha_type)}")

    # 获取新数据
    all_data = getGachaLogs(gacha_type)
    if not all_data:
        # continue
        raise Exception("获取祈愿记录失败")

    # 读取本地文件
    old_data = Read_GachaLogs_NewBetter(gacha_type)

    # 合并新数据并写入本地文件
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
            Update_NewBetter(gacha_type=ty[1])
        except Exception as ex:
            print(ex)
    print("update all done.")


# TODO
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
            pool_data = Read_GachaLogs_NewBetter(pool_id)
            pool_data.reverse()
            all_data[gacha_pools[pool_id]] = pool_data
        except Exception as g:
            print(g)
    return all_data


def Count_Five(local_data):
    """统计五星数量"""
    all_five = {}
    for pname in local_data:
        try:
            all_five[pname] = []
            gacha_times = 0 # 没五星的祈愿数量
            pool_data = local_data[pname]
            for data in pool_data:
                gacha_times += 1
                if data["rank_type"] == "5":
                    all_five[pname].append({"name": data["name"], "times": gacha_times})
                    gacha_times = 0
        except Exception as g:
            print(g)
    return all_five


def Print_Console(all_five: dict, export: bool = False):
    """输出五星统计表格到控制台"""
    all_ff = {}
    max_len = max([len(five) for five in all_five.values()])  # 5星最多的池子里5星数量
    for five in all_five:
        fives = all_five[five]
        all_ff[five] = [f"{f['name']}[{f['times']}]" for f in fives] # name[times]
        all_ff[five].extend([None] * (max_len - len(all_ff[five])))  # 长度对齐

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
    Print_Console(all_five, True)

    # See_LocalData(all_data)


if __name__ == "__main__":
    HOME_PATH = "GachaData"
    if not exists(HOME_PATH):
        mkdir(HOME_PATH)
    chdir(HOME_PATH)

    main()
