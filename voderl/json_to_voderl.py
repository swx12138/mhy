#

import json
from datetime import date
from time import time

import pandas
from regex import T


def readGachaLogsNb(gacha_type: int):
    """读取本地抽卡记录"""
    with open(
        "GachaData\\" + str(gacha_type) + "_nb.json", "r", encoding="utf-8"
    ) as file:
        return json.load(fp=file)


def read_loacl_json(id):
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

    return pandas.DataFrame(baeuty_data)


# 时间 名称 类别 星级 总次数 保底内

# https://voderl.github.io/genshin-gacha-analyzer/pools.js

if __name__ == "__main__":
    gacha_ty = {301: "角色活动祈愿", 302: "武器活动祈愿", 200: "常驻", 100: "新手祈愿"}
    with pandas.ExcelWriter(
        f"GachaData\\xlsx\\{date.today().__str__().replace('-','')}_fake.xlsx"
    ) as ex:
        for t in gacha_ty:
            read_loacl_json(t).to_excel(
                ex,
                gacha_ty[t],
                index=False,
                encoding="utf-8",
            )

        # 列宽20 10 5 5 6 6
        # 不需要save
        # ex.save()
