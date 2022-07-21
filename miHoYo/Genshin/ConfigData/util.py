#

import json


def OpenJsonFile(filename: str) -> json:
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


TextMap = OpenJsonFile(r"GenshinData\TextMap\TextMapCHS.json")


def getTextMap(hash: int):
    try:
        return TextMap[str(hash)]
    except KeyError:
        return ""
