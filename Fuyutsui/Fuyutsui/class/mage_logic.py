# -*- coding: utf-8 -*-
"""法师职业的基础逻辑（未实现）。"""

from utils import *

def run_mage_logic(state_dict, spec_name):
    spells = state_dict.get("spells") or {}
    生命值 = state_dict.get("生命值")
    能量值 = state_dict.get("能量值")
    一键辅助 = state_dict.get("一键辅助")
    目标有效 = state_dict.get("目标有效")
    战斗 = state_dict.get("战斗")
    施法 = state_dict.get("施法")
    引导 = state_dict.get("引导")
    移动 = state_dict.get("移动")
    英雄天赋 = state_dict.get("英雄天赋", 0)
    法术失败 = state_dict.get("法术失败", 0)
    首领战 = state_dict.get("首领战", 0)
    难度 = state_dict.get("难度", 0)
    施法技能 = state_dict.get("施法技能", 0)

    action_hotkey = None
    current_step = "无匹配技能"
    unit_info = {}

    if spec_name == "奥术":
        current_step = "奥术专精,不执行任何操作"
        return None, current_step, unit_info
    elif spec_name == "火焰":
        current_step = "火焰专精,不执行任何操作"
        return None, current_step, unit_info
    elif spec_name == "冰霜":
        真能真空 = state_dict.get("真能真空", 0)
        冰川尖刺 = state_dict.get("冰川尖刺", 0)
        冰冷智慧 = state_dict.get("冰冷智慧", 0)
        冰冻之雨 = state_dict.get("冰冻之雨", 0)
        寒冰指 = state_dict.get("寒冰指", 0)
        寒冰指层数 = state_dict.get("寒冰指层数", 0)
        敌人人数 = state_dict.get("敌人人数", 0)

        解除诅咒cd = spells.get("解除诅咒", -1)
        强化隐形术cd = spells.get("强化隐形术", -1)
        冰霜新星cd = spells.get("冰霜新星", -1)
        法术反制cd = spells.get("法术反制", -1)
        寒冰宝珠cd = spells.get("寒冰宝珠", -1)
        冰霜射线cd = spells.get("冰霜射线", -1)
        寒冰护体cd = spells.get("寒冰护体", -1)
        冰风暴cd = spells.get("冰风暴", -1)
        冰风暴充能cd = spells.get("冰风暴充能", -1)
        暴风雪Tcd = spells.get("暴风雪T", -1)
        暴风雪Ccd = spells.get("暴风雪C", -1)
        # 施放冰川尖刺时, 冰川尖刺层数清零,防止重复施法
        if 施法技能 == 2: 
           冰川尖刺 = 1

        if 引导 > 0:
            current_step = "在引导,不执行任何操作"
        
        elif 战斗 and 目标有效:
            if 敌人人数 > 3 and 冰冻之雨 > 0 and (暴风雪Tcd == 0 or 暴风雪Ccd == 0):
                current_step = "施放 暴风雪"
                action_hotkey = get_hotkey(0, "暴风雪")
            elif 冰冷智慧 > 0 and 真能真空 == 0 and 冰风暴cd == 0:
                current_step = "施放 冰风暴"
                action_hotkey = get_hotkey(0, "冰风暴")
            elif 寒冰指层数 == 2:
                current_step = "施放 冰枪术"
                action_hotkey = get_hotkey(0, "冰枪术")
            elif 冰川尖刺 >= 2:
                current_step = "施放 寒冰箭"
                action_hotkey = get_hotkey(0, "寒冰箭")
            else:
                action_map = {
                    1: ("奥术智慧", "奥术智慧"),
                    2: ("寒冰箭", "寒冰箭"),
                    3: ("冰川尖刺", "寒冰箭"),
                    4: ("冰枪术", "冰枪术"),
                    5: ("冰霜射线", "冰霜射线"),
                    6: ("冰风暴", "冰风暴"),
                    7: ("寒冰宝珠", "寒冰宝珠"),
                    8: ("暴风雪", "暴风雪"),
                    9: ("霜火之箭", "寒冰箭"),
                    10: ("彗星风暴", "冰霜射线"),
                }
                tup = action_map.get(一键辅助)
                if tup:
                    current_step = f"施放 {tup[0]}"
                    action_hotkey = get_hotkey(0, tup[1])
                else:
                    current_step = "战斗中-无匹配技能"

    return action_hotkey, current_step, unit_info