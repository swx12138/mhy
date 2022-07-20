#

from .util import getTextMap, OpenJsonFile


def Avatar():
    """人物相关"""
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\AvatarExcelConfigData.json")
    for each in data:
        print("=" * 30, each["Id"], "=" * 30)
        print("FeatureTagGroupID", each["FeatureTagGroupID"])
        print("体型：", each["BodyType"])
        print("姓名:", getTextMap(each["NameTextMapHash"]))
        print("简介:", getTextMap(each["DescTextMapHash"]))
        print("\n")


def FettersLevel():
    """好感经验"""
    data = OpenJsonFile(
        r"GenshinData\ExcelBinOutput\AvatarFettersLevelExcelConfigData.json"
    )
    for each in data:
        print(f"{each['FetterLevel']}\t{each['NeedExp']}")


def Flycloak():
    """风之翼"""
    data = OpenJsonFile(
        r"GenshinData\ExcelBinOutput\AvatarFlycloakExcelConfigData.json"
    )
    for each in data:
        print("=" * 15, each["flycloakId"], "=" * 15)
        print("名称：", getTextMap(each["nameTextMapHash"]))
        print("简介", getTextMap(each["descTextMapHash"]))
        print("id", each["materialId"])
        print("\n")


def LevelNeedExp():
    """等级经验"""
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\AvatarLevelExcelConfigData.json")
    return data


def Skill():
    """技能名称"""
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\AvatarSkillExcelConfigData.json")
    for each in data:
        print("=" * 15, each["Id"], "=" * 15)
        print("名称:", getTextMap(each["NameTextMapHash"]))
        print("简介:", getTextMap(each["DescTextMapHash"]))
        print(each)
        print("\n")


def Talent():
    """命之座"""
    data = OpenJsonFile(r"GenshinData\ExcelBinOutput\AvatarTalentExcelConfigData.json")
    for each in data:
        # print("=" * 15, each["TalentId"], each["Icon"].split("_")[-2], "=" * 15)
        # print("名称", getTextMap(each["NameTextMapHash"]))
        # print("名称", getTextMap(each["DescTextMapHash"]))
        nameTextMapHash = each.pop('nameTextMapHash')
        each['name'] = getTextMap(nameTextMapHash)
        descTextMapHash = each.pop('descTextMapHash')
        each['desc'] = getTextMap(descTextMapHash)
    return data