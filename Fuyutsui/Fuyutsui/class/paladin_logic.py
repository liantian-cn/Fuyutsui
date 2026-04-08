# -*- coding: utf-8 -*-
"""圣骑士职业的逻辑决策（神圣）。"""

from utils import *

def run_paladin_logic(state_dict, spec_name):
    spells = state_dict.get("spells") or {}

    战斗 = state_dict.get("战斗")
    移动 = state_dict.get("移动")
    施法 = state_dict.get("施法")
    引导 = state_dict.get("引导")
    生命值 = state_dict.get("生命值")
    能量值 = state_dict.get("能量值")
    一键辅助 = state_dict.get("一键辅助")
    法术失败 = state_dict.get("法术失败", 0)
    目标有效 = state_dict.get("目标有效")
    队伍类型 = int(state_dict.get("队伍类型", 0) or 0)
    队伍人数 = int(state_dict.get("队伍人数", 0) or 0)
    首领战 = int(state_dict.get("首领战", 0) or 0)
    难度 = int(state_dict.get("难度", 0) or 0)
    英雄天赋 = int(state_dict.get("英雄天赋", 0) or 0)
    
    神圣能量 = state_dict.get("神圣能量") or 0

    def _failed_spell_logic():
        spell_map = {
            1: "盲目之光",
            2: "光环掌握",
            3: "自由祝福",
            4: "制裁之锤",
            5: "保护祝福",
            6: "圣盾术",
        }
        spell_name = spell_map.get(法术失败)

        if spell_name and spells.get(spell_name, -1) == 0:
            current_step = f"施放 {spell_name}"
            action_hotkey = get_hotkey(0, spell_name)
            return current_step, action_hotkey

        return None, None
    
    action_hotkey = None
    current_step = "无匹配技能"
    unit_info = {}

    if spec_name == "神圣":
        dispel_unit_magic, _ = get_unit_with_dispel_type(state_dict, 1)
        dispel_unit_disease, _ = get_unit_with_dispel_type(state_dict, 3)
        dispel_unit_poison, _ = get_unit_with_dispel_type(state_dict, 4)
        lowest_unit, lowest_unit_pct = get_lowest_health_unit(state_dict, 100)
        no_eternal_lowest_unit, no_eternal_lowest_unit_pct = get_lowest_health_unit_without_aura(state_dict, "永恒之火", health_threshold=101)
        count_units_below_health_90 = count_units_below_health(state_dict, 90)
        
        if 法术失败 != 0:
            current_step, action_hotkey = _failed_spell_logic()
        elif 队伍类型 == 46 and spells.get("清洁术", 0) == 0 and dispel_unit_magic is not None:
            current_step = f"施放 清毒术 on {dispel_unit_magic}"
            action_hotkey = get_hotkey(int(dispel_unit_magic), "清毒术")
        elif 队伍类型 == 46 and spells.get("清洁术", 0) == 0 and dispel_unit_disease is not None:
            current_step = f"施放 清毒术 on {dispel_unit_disease}"
            action_hotkey = get_hotkey(int(dispel_unit_disease), "清毒术")
        elif 队伍类型 == 46 and spells.get("清洁术", 0) == 0 and dispel_unit_poison is not None:
            current_step = f"施放 清毒术 on {dispel_unit_poison}"
            action_hotkey = get_hotkey(int(dispel_unit_poison), "清毒术")
        elif lowest_unit is not None and lowest_unit_pct is not None and lowest_unit_pct <= 95:
            if spells.get("圣疗术", 0) <= 1 and lowest_unit_pct < 25:
                current_step = f"施放 圣疗术 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "圣疗术")
            elif (神圣能量 == 5 or state_dict.get("神圣意志") > 0) and count_units_below_health_90 > 5:
                current_step = "施放 黎明之光"
                action_hotkey = get_hotkey(0, "黎明之光")
            elif (神圣能量 == 5 or state_dict.get("神圣意志") > 0) and count_units_below_health_90 <= 5:
                current_step = f"施放 荣耀圣令 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "荣耀圣令")
            elif spells.get("震击充能", 0) <= 1 and state_dict.get("圣光灌注") == 0:
                current_step = f"施放 神圣震击 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "神圣震击")
            elif 施法 == 0 and lowest_unit_pct < 70 and state_dict.get("神性之手") > 0:
                current_step = f"施放 圣光术 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "圣光术")
            elif (神圣能量 > 3 or state_dict.get("神圣意志") > 0) and lowest_unit_pct <= 60:
                current_step = f"施放 荣耀圣令 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "荣耀圣令")
            elif 神圣能量 > 3 and no_eternal_lowest_unit is not None and no_eternal_lowest_unit_pct is not None and no_eternal_lowest_unit_pct < 80:
                current_step = f"施放 荣耀圣令 on {no_eternal_lowest_unit}"
                action_hotkey = get_hotkey(int(no_eternal_lowest_unit), "荣耀圣令")
            elif spells.get("圣洁鸣钟") == 0 and 神圣能量 <= 2 and count_units_below_health_90 >= 3:
                current_step = "施放 圣洁鸣钟"
                action_hotkey = get_hotkey(0, "圣洁鸣钟")
            elif 施法 == 0 and state_dict.get("圣光灌注") > 0 and lowest_unit_pct < 80:
                current_step = f"施放 圣光闪现 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "圣光闪现")
            elif spells.get("神圣震击", 0) <= 1 and state_dict.get("圣光灌注") == 0:
                current_step = f"施放 神圣震击 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "神圣震击")
            elif 施法 == 0 and lowest_unit_pct < 50 and 能量值 >= 50:
                current_step = f"施放 圣光术 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "圣光术")
            elif 施法 == 0:
                current_step = f"施放 圣光闪现 on {lowest_unit}"
                action_hotkey = get_hotkey(int(lowest_unit), "圣光闪现")
            else:
                current_step = "无匹配技能"
        elif 战斗 and 目标有效:
            if 神圣能量 == 5 or state_dict.get("神圣意志") > 0:
                current_step = "施放 正义盾击"
                action_hotkey = get_hotkey(0, "正义盾击")
            elif spells.get("审判", 0) <= 1:
                current_step = "施放 审判"
                action_hotkey = get_hotkey(0, "审判")
            elif spells.get("神圣震击") == 0:
                current_step = "施放 神圣震击"
                action_hotkey = get_hotkey(0, "神圣震击")
        else:
            current_step = "无匹配技能"
 
    elif spec_name == "防护":
        if  法术失败 != 0:
            current_step, action_hotkey = _failed_spell_logic()
        elif 战斗 and 目标有效:
            if state_dict.get("军备类型") == 1 and spells.get("神圣壁垒") == 0 and state_dict.get("神圣壁垒") == 0:
                current_step = "施放 神圣壁垒"
                action_hotkey = get_hotkey(0, "神圣壁垒")
            elif state_dict.get("军备类型") == 2 and spells.get("神圣壁垒") == 0 and state_dict.get("圣洁武器") == 0:
                current_step = "施放 神圣壁垒"
                action_hotkey = get_hotkey(0, "神圣壁垒")
            elif state_dict.get("闪耀之光") > 0 and 生命值 < 80:
                current_step = "施放 荣耀圣令"
                action_hotkey = get_hotkey(0, "荣耀圣令")
            else:
                action_map = {
                    1: ("圣洁鸣钟", "圣洁鸣钟"),
                    2: ("复仇者之盾", "复仇者之盾"),
                    3: ("奉献", "奉献"),
                    4: ("审判", "审判"),
                    5: ("正义盾击", "正义盾击"),
                    6: ("祝福之锤", "祝福之锤"),
                    15: ("愤怒之锤", "审判"),
                }
                tup = action_map.get(一键辅助)
                if tup and spells.get(tup[0], 0) <= 1:
                    current_step = f"施放 {tup[0]}"
                    action_hotkey = get_hotkey(0, tup[1])
                else:
                    current_step = "战斗中-无匹配技能"

    elif spec_name == "惩戒":
        if  法术失败 != 0:
            current_step, action_hotkey = _failed_spell_logic()
        elif 战斗 and 目标有效:
            action_map = {
                7: ("公正之剑", "公正之剑"),
                1: ("圣洁鸣钟", "圣洁鸣钟"),
                8: ("审判", "审判"),
                9: ("最终审判", "最终审判"),
                10: ("灰烬觉醒", "灰烬觉醒"),
                11: ("神圣风暴", "神圣风暴"),
                12: ("圣光之锤", "灰烬觉醒"),
                13: ("愤怒之锤", "审判"),
                14: ("处决宣判", "处决宣判"),
            }
            tup = action_map.get(一键辅助)
            if tup:
                current_step = f"施放 {tup[0]}"
                action_hotkey = get_hotkey(0, tup[1])
            else:
                current_step = "战斗中-无匹配技能"

    return action_hotkey, current_step, unit_info
