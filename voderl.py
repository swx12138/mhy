#

import json
from os import chdir, mkdir

import pandas
from genericpath import exists

from ExportGachaLogs import Read_GachaLogs_NewBetter


def read_loacl_json(id):
    all_data = Read_GachaLogs_NewBetter(id)
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


def ExportExcel():
    gacha_ty = {301: "角色活动祈愿", 302: "武器活动祈愿", 200: "常驻", 100: "新手祈愿"}
    with pandas.ExcelWriter(f"voderl_fake.xlsx") as ex:
        for t in gacha_ty:
            read_loacl_json(t).to_excel(
                ex,
                gacha_ty[t],
                index=False,
                encoding="utf-8",
            )


def ImportExcel():
    print("reading.")
    pd = pd.read_excel(
        "xlsx\\20220718_225556.xlsx",
        sheet_name=["角色活动祈愿", "武器活动祈愿", "常驻祈愿", "新手祈愿"],
    )

    for item in [
        ("角色活动祈愿", "301"),
        ("武器活动祈愿", "302"),
        ("常驻祈愿", "200"),
        ("新手祈愿", "100"),
    ]:
        all_data = []
        for lable, gacha in pd[item[0]].iterrows():
            all_data.append(
                {
                    "uid": "100266228",
                    "gacha_type": item[1],
                    "item_id": "",
                    "count": "1",
                    "time": gacha[0],
                    "name": gacha[1],
                    "lang": "zh-cn",
                    "item_type": gacha[2],
                    "rank_type": str(gacha[3]),
                    "id": "0",
                }
            )
        all_data.reverse()
        with open(item[1] + "_export.json", "w", encoding="utf-8") as file:
            json.dump(all_data, fp=file, ensure_ascii=False, indent=4)


# TODO
# 时间 名称 类别 星级 总次数 保底内
# 列宽20 10 5 5 6 6
# https://voderl.github.io/genshin-gacha-analyzer/pools.js


if __name__ == "__main__":
    HOME_PATH = "GachaData"
    if not exists(HOME_PATH):
        mkdir(HOME_PATH)
    chdir(HOME_PATH)

    ExportExcel()
