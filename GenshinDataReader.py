import itertools
import json

import pylab as lab
from pandas import DataFrame, ExcelWriter
from styleframe import StyleFrame, Styler

from miHoYo.Genshin import ConfigData
from miHoYo.Genshin.ConfigData.util import getTextMap


def make_weapon_level_curve():
    data = ConfigData.Weapon.LevelExcel()
    s1 = sum(data["White"])
    s2 = sum(data["Green"])
    s3 = sum(data["Blue"])
    s4 = sum(data["Purple"])
    s5 = sum(data["Golden"])

    x = [i for i in range(0, 90)]
    lab.plot(x, list(itertools.accumulate(data["White"])), color="black")
    lab.plot(x, list(itertools.accumulate(data["Green"])), color="green")
    lab.plot(x, list(itertools.accumulate(data["Blue"])), color="blue")
    lab.plot(x, list(itertools.accumulate(data["Purple"])), color="purple")
    lab.plot(x, list(itertools.accumulate(data["Golden"])), color="yellow")
    # lab.show()
    lab.gcf().set_size_inches(27, 35)
    lab.savefig("weapon_level_exp_1.png")


def char_level_curve():
    exp = ConfigData.Avatar.LevelNeedExp()
    # exp = DataFrame(exp)
    # print(exp)
    x = [e['level'] for e in exp]
    y = list(itertools.accumulate([e['exp'] for e in exp]))
    # print(x,y)
    lab.plot(x, y)
    lab.show()

def pick_sp():
    picked = {
        "unreleased": [],
        "hidden": [],
    }
    with open(r"GenshinData\TextMap\TextMapCHS.json", 'r', encoding="utf-8",) as file:
        data = json.load(file)
        filter = [
            {"name": 'unreleased', "val": '$UNRELEASED'},
            {"name": 'hidden', "val": '$HIDDEN'},
        ]
        for id in data:
            word: str = data[id]
            for keyword in filter:
                if -1 != word.find(keyword['val']):
                    picked[keyword["name"]].append(word)

    with ExcelWriter("words.xlsx") as w:
        styler = Styler(
            #bg_color='gray',
            #font_color='green',
            horizontal_alignment='left',
            wrap_text=False
        )
        for pi in picked:
            sf = StyleFrame(
                obj=DataFrame(picked[pi]),
                styler_obj=styler,
                columns=['A']
            )
            sf.set_column_width('A', width=150)
            sf.to_excel(excel_writer=w, sheet_name=pi, encoding="utf-8",)


if __name__ == "__main__":
    # ConfigData.Weapon.AllWeapon()
    # talents = ConfigData.Avatar.Talent()
    # characters = []
    # for talent in talents:
    #     characters.append(talent["openConfig"].split('_')[0])
    #     if characters[-1] == 'Yelan':
    #         print(talent["desc"])
    # print(list(set(characters)))
    # ConfigData.Avatar.Flycloak()
    ac = ConfigData.Achievement.Achievement()
    DataFrame([(a["titleTextMapHash"],a["descTextMapHash"]) for a in ac]).to_excel("achievement.xlsx")
