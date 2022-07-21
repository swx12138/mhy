#

from .util import getTextMap, OpenJsonFile

def AchievementGoal():
    """成就大分类"""
    data = OpenJsonFile("GenshinData\ExcelBinOutput\AchievementGoalExcelConfigData.json") 
    for d in data:
        d["nameTextHash"] = getTextMap(d["nameTextHash"])
    return data

def Achievement():
    data = OpenJsonFile("GenshinData\ExcelBinOutput\AchievementExcelConfigData.json")
    for d in data:
        d["titleTextMapHash"] = getTextMap(d["titleTextMapHash"])
        d["descTextMapHash"] = getTextMap(d["descTextMapHash"])
    return data