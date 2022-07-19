#

from .util import getTextMap, OpenJsonFile


def LevelExcel():
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\WeaponLevelExcelConfigData.json")
    ret = {
        "White": [0] * 90,
        "Green": [0] * 90,
        "Blue": [0] * 90,
        "Purple": [0] * 90,
        "Golden": [0] * 90,
    }
    for d in data:
        id = d["Level"] - 1
        ret["White"][id] = d["RequiredExps"][0]
        ret["Green"][id] = d["RequiredExps"][1]
        ret["Blue"][id] = d["RequiredExps"][2]
        ret["Purple"][id] = d["RequiredExps"][3]
        ret["Golden"][id] = d["RequiredExps"][4]
    return ret


def AllWeapon():
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\WeaponExcelConfigData.json")
    for d in data:
        print("=" * 15, "名称:", getTextMap(d["NameTextMapHash"]), "=" * 15)
        print("type:", d["WeaponType"])
        print("desc:", getTextMap(d["DescTextMapHash"]))
        print("")
