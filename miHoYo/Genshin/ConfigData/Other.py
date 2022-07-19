#

from .util import getTextMap, OpenJsonFile


def RandomMainQuest():
    """随机任务"""
    data = OpenJsonFile(
        r"GenshinData\[Obfuscated] ExcelBinOutput\RandomMainQuestExcelConfigData.json"
    )
    for each in data:
        print("=" * 20, "id:", each["_id"], "=" * 20)
        print("type:", each["_type"])
        print("title:", getTextMap(each["_titleTextMapHash"]))
        print("desc:", getTextMap(each["_descTextMapHash"]))
        print("\n")


def RandomQuest():
    data = OpenJsonFile(
        r"GenshinData\[Obfuscated] ExcelBinOutput\RandomQuestExcelConfigData.json"
    )
    for each in data:
        print(getTextMap(each["_titleTextMapHash"]))


def UidOpNotify():
    """活动相关文本"""
    data = OpenJsonFile(
        r"GenshinData\[Obfuscated] ExcelBinOutput\UidOpNotifyExcelConfigData.json"
    )
    for each in data:
        print("=" * 20, each["MEGIDKNJNOH"], "=" * 20)
        print(getTextMap(each["KICAAJNHJJK"]))
        print("\n")


def RoguelikeCard():
    """Roguelike buff卡配置"""
    data = OpenJsonFile(
        r"GenshinData\[Obfuscated] ExcelBinOutput\RoguelikeCardExcelConfigData.json"
    )
    for each in data:
        print("=" * 15, getTextMap(each["DHHKCOLFCBP"]), "=" * 15)
        print(each["CCIGEMGAAOF"])
        print(getTextMap(each["LGLEADJKBGN"]))
        print(getTextMap(each["OGLDGDCHFDL"]))
        print("\n")


def Bargain():
    """议价"""
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\BargainExcelConfigData.json")
    for each in data:
        print("=" * 15, each["QuestId"], "=" * 15)
        print("MoodLowLimitText:", getTextMap(each["MoodLowLimitTextTextMapHash"]))
        print("TitleText:", getTextMap(each["TitleTextTextMapHash"]))
        print("AffordText:", getTextMap(each["AffordTextTextMapHash"]))
        print("StorageText:", getTextMap(each["StorageTextTextMapHash"]))
        print("MoodHintText:", getTextMap(each["MoodHintTextTextMapHash"]))
        print("MoodDescText:", getTextMap(each["MoodDescTextTextMapHash"]))
        print("\n")


def BookSuit():
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\BookSuitExcelConfigData.json")
    for d in data:
        print("=" * 15, d["Id"], "=" * 15)
        print("BookSuit:", getTextMap(d["SuitNameTextMapHash"]))
