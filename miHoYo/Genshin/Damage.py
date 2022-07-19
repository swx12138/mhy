
# 参考自NGA
# https://bbs.nga.cn/read.php?tid=25564438

from abc import abstractmethod
import numpy as np


class ISection:
    @abstractmethod
    def Number(this):
        pass


class Attack(ISection):
    '''攻击区'''
    def __init__(this, base: int, weapon: int, buff: float, extern: int) -> None:
        super().__init__()
        this.__White = base + weapon
        this.__Green = this.__White * (1 + buff) + extern

    def Number(this) -> float:
        return this.__White + this.__Green


class Multipiler(ISection):
    '''倍率区'''
    def __init__(this, ablity_rate: list, independent: float) -> None:
        '''
        ablity_rate - 技能倍率
        independent - 独立乘区
        '''
        super().__init__()
        this.__Mul = sum(ablity_rate) * (1 + independent)

    def Number(this):
        return this.__Mul


class Bouns(ISection):
    '''增伤区'''
    def __init__(this, bouns: list) -> None:
        super().__init__()
        this.__Bouns = 1 + sum(bouns)

    def Number(this):
        return this.__Bouns


class Critical(ISection):
    '''爆伤区'''
    def __init__(this, crit: float, crit_dmg: float) -> None:
        super().__init__()
        if crit > 5:
            crit /= 100
        if crit_dmg > 100:
            crit_dmg /= 100
        this.__Bouns = 1 + crit * crit_dmg

    def Number(this):
        return this.__Bouns


class Reaction(ISection):
    '''反应区'''
    def __init__(this, base, ElementMastery, Up) -> None:
        '''
        base - 基础反应倍率
        ElementMastery - 元素精通
        Up - 反应系数提升（一般为圣遗物提升）
        '''
        super().__init__()
        this.__EM = 2.78 * ElementMastery / (ElementMastery + 1400)
        this.__Bouns = base * (1 + this.__EM + Up)

    def Number(this):
        return this.__Bouns


class Defense(ISection):
    '''防御区 暂时不使用'''
    def __init__(this, IngLevel, EdLevel, DefBuf) -> None:
        '''
        IngLevel - 人物等级
        EdLevel - 怪物等级
        '''
        super().__init__()
        this.__IngLevel = IngLevel + 100
        this.__EdLevel = EdLevel + 100
        this.__Defbuf = 1 + DefBuf

    def Number(this):
        return this.__IngLevel/(this.__Defbuf * (this.__IngLevel+this.__EdLevel))


class Resistance(ISection):
    '''抗性区'''
    def __init__(this, YuanKangxing, JianKang, JiaKang) -> None:
        super().__init__()
        this.__R = YuanKangxing - JianKang + JiaKang

    def Number(this):
        if this.__R > 0.75:
            return 1/(this.__R*4+1)
        elif this.__R < 0:
            return 1 - this.__R/2
        else:
            return 1 - this.__R


class Character:
    def __init__(this, attack: Attack, multipiler: Multipiler, bouns: Bouns, crit: Critical, reaction: Reaction, defense: Defense, res: Resistance) -> None:
        this.__Attack = attack
        this.__Bouns = bouns
        this.__Critical = crit
        this.__Reaction = reaction
        this.__Defense = defense
        this.__Resistance = res
        this.Set_Multipiler(multipiler)

    def Calcu(this):
        ls = [
            this.__Attack.Number(),
            this.__Multipiler.Number(),
            this.__Bouns.Number(),
            this.__Critical.Number(),
            this.__Reaction.Number(),
            this.__Defense.Number(),
            this.__Resistance.Number()]
        return np.prod(ls)

    def Set_Multipiler(this, multipiler: Multipiler):
        this.__Multipiler = multipiler

def EzCalcu(atk,crit,crit_dmg,bouns:list):
    Eula = Character(
        attack=Attack(0, 0, 0, atk),
        multipiler=Multipiler([1], 0),
        bouns=Bouns(bouns),
        crit=Critical(crit, crit_dmg),
        reaction=Reaction(1, 0, 0),
        defense=Defense(90, 100,0),
        res=Resistance(0.1, 0,0)
    )
    return Eula.Calcu()