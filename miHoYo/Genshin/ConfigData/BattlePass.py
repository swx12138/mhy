#

from .util import getTextMap, OpenJsonFile


def Schedule():
    data = OpenJsonFile(
        r"GenshinData\ExcelBinOutput\BattlePassScheduleExcelConfigData.json"
    )
    for d in data:
        print("=" * 15, d["Id"], "=" * 15)
        print("标题:", getTextMap(d["TitleNameTextMapHash"]))
        print(d["BeginDateStr"], " - ", d["EndDateStr"])
        print("持续时间", sum(d["CycleList"]))
        print("\n")
