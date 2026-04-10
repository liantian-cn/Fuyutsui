# -*- coding: utf-8 -*-
"""牧师职业的逻辑决策（戒律 / 神牧 / 暗影）。"""

from utils import *

# 戒律
def _priest_discipline_logic(state_dict):
    spells = state_dict.get("spells") or {}
    生命值 = state_dict.get("生命值")
    能量值 = state_dict.get("能量值")
    一键辅助 = state_dict.get("一键辅助")
    目标有效 = state_dict.get("目标有效")
    战斗 = state_dict.get("战斗")
    施法 = state_dict.get("施法")
    引导 = state_dict.get("引导")
    移动 = state_dict.get("移动")
    队伍类型 = int(state_dict.get("队伍类型", 0) or 0)
    英雄天赋 = int(state_dict.get("英雄天赋", 0) or 0)
    首领战 = int(state_dict.get("首领战", 0) or 0)

    action_hotkey = None
    current_step = "无匹配技能"
    unit_info = {}

    福音cd = spells.get("福音", -1)
    耀cd = spells.get("真言术：耀", -1)
    盾cd = spells.get("真言术：盾", -1)
    苦修cd = spells.get("苦修", -1)
    灭cd = spells.get("暗言术：灭", -1)
    心灵震爆cd = spells.get("心灵震爆", -1)

    熵能裂隙 = state_dict.get("熵能裂隙", 0)
    圣光涌动 = state_dict.get("圣光涌动", 0)
    虚空之盾 = state_dict.get("虚空之盾", -1)
    福音层数 = state_dict.get("福音层数", 0)
    法术失败 = state_dict.get("法术失败", 0)

    dispel_unit, _ = get_unit_with_dispel_type(state_dict, 1)
    lowest_u, lowest_p = get_lowest_health_unit(state_dict, 100)
    no_ato_u, no_ato_p = get_lowest_health_unit_without_aura(state_dict, "救赎", 100)
    no_shd_lowest_u, no_shd_lowest_p = get_lowest_health_unit_without_aura(state_dict, "真言术：盾", 100)
    no_shd_u, no_shd_p = get_lowest_health_unit_without_aura(state_dict, "真言术：盾", 100)
    no_shd_tank, no_shd_tank_pct = get_unit_with_role_and_without_aura_name(state_dict, 1, "真言术：盾")
    no_ato_count_90 = count_units_without_aura_below_health(state_dict, "救赎", 90)
    atonement_count = count_units_with_aura(state_dict, "救赎")

    unit_info = {
        "dispel_unit": dispel_unit,
        "lowest_unit": lowest_u,
        "lowest_unit_pct": lowest_p,
        "no_atonement_unit": no_ato_u,
        "no_atonement_pct": no_ato_p,
        "no_shield_lowest_unit": no_shd_lowest_u,
        "no_shield_lowest_pct": no_shd_lowest_p,
        "no_shield_unit": no_shd_u,
        "no_shield_pct": no_shd_p,
        "no_atonement_count_90": no_ato_count_90,
        "atonement_count": atonement_count,
    }

    if 引导 > 0:
        current_step = "引导,不执行任何操作"
    elif spells.get("绝望祷言") == 0 and 生命值 < 50:
        current_step = "施放 绝望祷言"
        action_hotkey = get_hotkey(0, "绝望祷言")
    elif spells.get("奥术洪流") == 0 and 能量值 <= 90:
        current_step = "施放 奥术洪流"
        action_hotkey = get_hotkey(0, "奥术洪流")
    elif 一键辅助 == 1:
        current_step = "施放 真言术：韧"
        action_hotkey = get_hotkey(0, "真言术：韧")
    elif spells.get("心灵尖啸") < 1 and 法术失败 == 1:
        current_step = "施放 心灵尖啸"
        action_hotkey = get_hotkey(0, "心灵尖啸")
    elif spells.get("群体驱散") < 1 and 法术失败 == 2:
        current_step = "施放 群体驱散"
        action_hotkey = get_hotkey(0, "群体驱散")
    elif spells.get("真言术：障") < 1 and 法术失败 == 3:
        current_step = "施放 真言术：障"
        action_hotkey = get_hotkey(0, "真言术：障")
    elif spells.get("终极苦修") < 1 and 法术失败 == 4:
        current_step = "施放 终极苦修"
        action_hotkey = get_hotkey(0, "终极苦修")
    elif 英雄天赋 == 1:
        if 队伍类型 <= 40:
            if 福音cd == 0 and no_ato_count_90 >= 4:
                current_step = "施放 福音"
                action_hotkey = get_hotkey(0, "福音")
            elif 耀cd == 0 and no_ato_count_90 >= 4 and 福音层数 > 0:
                current_step = "施放 真言术：耀"
                action_hotkey = get_hotkey(0, "真言术：耀")
            elif 目标有效 and 战斗 and 一键辅助 == 5:
                current_step = "施放 暗言术：痛"
                action_hotkey = get_hotkey(0, "暗言术：痛")
            elif 圣光涌动 > 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                current_step = f"施放 快速治疗 on {no_ato_u}, 无救赎生命低于90%的单位"
                action_hotkey = get_hotkey(int(no_ato_u), "快速治疗")
            elif 圣光涌动 > 0 and lowest_u is not None and lowest_p is not None and lowest_p < 70:
                current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
            elif 盾cd == 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎单位"
                action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")
            elif 盾cd == 0 and no_shd_lowest_u is not None and no_shd_lowest_p is not None and no_shd_lowest_p < 90:
                current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
            elif 盾cd == 0 and no_shd_tank is not None:
                current_step = f"施放 真言术：盾 on {no_shd_tank}, 无盾单位"
                action_hotkey = get_hotkey(int(no_shd_tank), "真言术：盾")
            elif 盾cd == 0 and no_shd_lowest_u is not None:
                current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
            elif 耀cd == 0 and 施法 == 0 and no_ato_count_90 >= 5:
                current_step = "施放 真言术：耀"
                action_hotkey = get_hotkey(0, "真言术：耀")
            elif 苦修cd == 0 and lowest_u is not None and lowest_p is not None and lowest_p < 75:
                current_step = f"施放 苦修 on {lowest_u}, 生命最低的单位"
                action_hotkey = get_hotkey(int(lowest_u), "苦修")
            elif 目标有效 and 战斗:
                if 灭cd == 0:
                    current_step = "施放 暗言术：灭"
                    action_hotkey = get_hotkey(0, "暗言术：灭")
                elif not 移动 and 心灵震爆cd == 0:
                    current_step = "施放 心灵震爆"
                    action_hotkey = get_hotkey(0, "心灵震爆")
                elif 苦修cd == 0:
                    current_step = "施放 苦修"
                    action_hotkey = get_hotkey(0, "苦修")
                elif not 移动:
                    current_step = "施放 惩击"
                    action_hotkey = get_hotkey(0, "惩击")
                else:
                    current_step = "战斗中-无匹配技能"
        elif 队伍类型 == 46:
            if spells.get("纯净术") == 0 and dispel_unit is not None:
                current_step = f"施放 纯净术 on {dispel_unit}"
                action_hotkey = get_hotkey(int(dispel_unit), "纯净术")
            elif 福音cd == 0 and no_ato_count_90 >= 4:
                current_step = "施放 福音"
                action_hotkey = get_hotkey(0, "福音")
            elif 耀cd == 0 and no_ato_count_90 >= 4 and 福音层数 > 0:
                current_step = "施放 真言术：耀"
                action_hotkey = get_hotkey(0, "真言术：耀")
            elif 目标有效 and 战斗 and 一键辅助 == 5:
                current_step = "施放 暗言术：痛"
                action_hotkey = get_hotkey(0, "暗言术：痛")
            elif 圣光涌动 > 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                current_step = f"施放 快速治疗 on {no_ato_u}, 无救赎生命低于90%的单位"
                action_hotkey = get_hotkey(int(no_ato_u), "快速治疗")
            elif 圣光涌动 > 0 and lowest_u is not None and lowest_p is not None and lowest_p < 70:
                current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
            elif 盾cd == 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎单位"
                action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")
            elif 盾cd == 0 and no_shd_lowest_u is not None and no_shd_lowest_p is not None and no_shd_lowest_p < 90:
                current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
            elif 盾cd == 0 and no_shd_tank is not None:
                current_step = f"施放 真言术：盾 on {no_shd_tank}, 无盾单位"
                action_hotkey = get_hotkey(int(no_shd_tank), "真言术：盾")
            elif 盾cd == 0 and no_shd_lowest_u is not None:
                current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
            elif 耀cd == 0 and 施法 == 0 and no_ato_count_90 >= 5:
                current_step = "施放 真言术：耀"
                action_hotkey = get_hotkey(0, "真言术：耀")
            elif 苦修cd == 0 and lowest_u is not None and lowest_p is not None and lowest_p < 75:
                current_step = f"施放 苦修 on {lowest_u}, 生命最低的单位"
                action_hotkey = get_hotkey(int(lowest_u), "苦修")
            elif 目标有效 and 战斗:
                if 灭cd == 0:
                    current_step = "施放 暗言术：灭"
                    action_hotkey = get_hotkey(0, "暗言术：灭")
                elif not 移动 and 心灵震爆cd == 0:
                    current_step = "施放 心灵震爆"
                    action_hotkey = get_hotkey(0, "心灵震爆")
                elif 苦修cd == 0:
                    current_step = "施放 苦修"
                    action_hotkey = get_hotkey(0, "苦修")
                elif not 移动:
                    current_step = "施放 惩击"
                    action_hotkey = get_hotkey(0, "惩击")
                else:
                    current_step = "战斗中-无匹配技能"

    elif 英雄天赋 == 2:
        if 战斗:
            if 目标有效 and 一键辅助 == 5:
                current_step = "施放 暗言术：痛"
                action_hotkey = get_hotkey(0, "暗言术：痛")
            elif 目标有效 and 熵能裂隙 > 0 and 苦修cd == 0:
                current_step = "施放 苦修"
                action_hotkey = get_hotkey(0, "苦修")
            elif 盾cd == 0  and no_ato_u is not None and no_ato_p < 99:
                current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎生命最低的单位, 有虚空之盾"
                action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")
            elif 圣光涌动 > 0 and no_ato_u is not None and no_ato_p < 90:
                current_step = f"施放 快速治疗 on {no_ato_u}, 无救赎生命低于90%的单位"
                action_hotkey = get_hotkey(int(no_ato_u), "快速治疗")
            elif 福音cd == 0 and (no_ato_count_90 >= 4 or (队伍类型 == 46 and no_ato_count_90 >= 1)):
                current_step = "施放 福音"
                action_hotkey = get_hotkey(0, "福音")
            elif 耀cd == 0 and 施法 == 0 and (no_ato_count_90 >= 4 or (队伍类型 == 46 and no_ato_count_90 >= 1)):
                current_step = "施放 真言术：耀"
                action_hotkey = get_hotkey(0, "真言术：耀")
            elif 灭cd == 0:
                current_step = "施放 暗言术：灭"
                action_hotkey = get_hotkey(0, "暗言术：灭")
            elif not 移动 and 心灵震爆cd == 0:
                current_step = "施放 心灵震爆"
                action_hotkey = get_hotkey(0, "心灵震爆")
            elif not 移动 and 目标有效 and 熵能裂隙 > 0:
                current_step = "施放 惩击"
                action_hotkey = get_hotkey(0, "惩击")
            elif 盾cd == 0 and no_ato_u is not None and no_ato_p < 90:
                current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎生命最低的单位"
                action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")   
            elif 目标有效 and 苦修cd == 0 and 虚空之盾 == 0:
                current_step = "施放 苦修"
                action_hotkey = get_hotkey(0, "苦修")
            elif 目标有效:
                current_step = "施放 惩击"
                action_hotkey = get_hotkey(0, "惩击")
    return action_hotkey, current_step, unit_info

# 神圣
def _priest_holy_logic(state_dict):
    action_hotkey = None
    current_step = "无匹配技能"
    unit_info = {}

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

    施法技能 = state_dict.get("施法技能", 0)
    施法目标 = state_dict.get("施法目标", 0)

    织光者 = state_dict.get("织光者", 0)
    织光层数 = state_dict.get("织光层数", 0)
    圣光涌动 = state_dict.get("圣光涌动", 0)
    祈福 = state_dict.get("祈福", 0)
    
    愈合祷言_cd = spells.get("愈合祷言", -1)
    静_cd = spells.get("圣言术：静", -1)
    静_charge = spells.get("静充能", -1)
    罚_cd = spells.get("圣言术：罚", -1)
    纯净术_cd = spells.get("纯净术", -1)
    绝望祷言_cd = spells.get("绝望祷言", -1)
    神圣化身_cd = spells.get("神圣化身", -1)
    光晕_cd = spells.get("光晕", -1)
    神圣赞美诗_cd = spells.get("神圣赞美诗", -1)
    神圣之火_cd = spells.get("神圣之火", -1)
    心灵尖啸_cd = spells.get("心灵尖啸", -1)
    群体驱散_cd = spells.get("群体驱散", -1)
    奥术洪流_cd = spells.get("奥术洪流", -1)

    dispel_magic_unit, _ = get_unit_with_dispel_type(state_dict, 1)
    dispel_unit_disease, _ = get_unit_with_dispel_type(state_dict, 3)
    lowest_u, lowest_p = get_lowest_health_unit(state_dict, 100)
    no_mend_u, no_mend_p = get_lowest_health_unit_without_aura(state_dict, "愈合祷言", 101)
    no_mend_tank, no_mend_tank_pct = get_unit_with_role_and_without_aura_name(state_dict, 1, "愈合祷言")
    count90 = get_count_units_below_health(state_dict, 90)
    count80 = get_count_units_below_health(state_dict, 80)

    if 施法技能 == 11 and 织光层数 > 0:
        织光层数 -= 1
    if 施法技能 == 4 or 施法技能 == 19:
        织光层数 += 1

    驱散单位 = None
    if dispel_magic_unit is not None:
        if 队伍类型 == 46 and 首领战 not in no_dispel_bosses:
            驱散单位 = dispel_magic_unit
        elif 队伍类型 <= 40 and 首领战 in need_dispel_bosses:
            驱散单位 = dispel_magic_unit
    if 驱散单位 is None:
        驱散单位 = dispel_unit_disease
    
    治疗限值 = int(60 + (能量值 * 0.3)) # 90-60
    群疗限值数量 = get_count_units_below_health(state_dict, 治疗限值)
    群疗限值2数量 = get_count_units_below_health(state_dict, 治疗限值 - 10)

    # 战斗逻辑
    def _combat_filler():
        nonlocal current_step, action_hotkey
        if not 移动 and 神圣之火_cd == 0:
            current_step = "施放 神圣之火"
            action_hotkey = get_hotkey(0, "神圣之火")
        elif not 移动:
            current_step = "施放 惩击"
            action_hotkey = get_hotkey(0, "惩击")
        else:
            current_step = "战斗中-无匹配技能"

    # 愈合祷言逻辑
    def _mending_filler():
        nonlocal current_step, action_hotkey
        if 愈合祷言_cd == 0 and no_mend_u is not None and no_mend_p is not None and no_mend_p < 95:
            current_step = f"施放 愈合祷言 on {no_mend_u}, 无愈合祷言生命低于95%的单位"
            action_hotkey = get_hotkey(int(no_mend_u), "愈合祷言")
        elif 愈合祷言_cd == 0 and no_mend_tank is not None:
            current_step = f"施放 愈合祷言 on {no_mend_tank}, 无愈合祷言坦克"
            action_hotkey = get_hotkey(int(no_mend_tank), "愈合祷言")
        elif 愈合祷言_cd == 0 and no_mend_u is not None:
            current_step = f"施放 愈合祷言 on {no_mend_u}, 无愈合祷言的单位"
            action_hotkey = get_hotkey(int(no_mend_u), "愈合祷言")
        else:
            current_step = f"施放 愈合祷言 on 玩家"
            action_hotkey = get_hotkey(1, "愈合祷言")

    # 法术失败逻辑
    def _failed_spell_logic():
        spell_map = {
            1: "心灵尖啸",
            2: "群体驱散",
            5: "神圣化身",
            6: "光晕",
            7: "神圣赞美诗",
        }
        spell_name = spell_map.get(法术失败)

        if spell_name and spells.get(spell_name, -1) == 0:
            current_step = f"施放 {spell_name}"
            action_hotkey = get_hotkey(0, spell_name)
            return current_step, action_hotkey

        return None, None
        
    # 将需要驱散的首领 ID
    need_dispel_bosses = {4, 5}
    # 不需要驱散的首领 ID
    no_dispel_bosses = {64}

    if 引导 > 0:
        current_step = "引导,不执行任何操作"
    elif 绝望祷言_cd == 0 and 生命值 < 50:
        current_step = "施放 绝望祷言"
        action_hotkey = get_hotkey(0, "绝望祷言")
    elif 奥术洪流_cd == 0 and 能量值 <= 90:
        current_step = "施放 奥术洪流"
        action_hotkey = get_hotkey(0, "奥术洪流")
    elif 一键辅助 == 1:
        current_step = "施放 真言术：韧"
        action_hotkey = get_hotkey(0, "真言术：韧")
    elif 法术失败 != 0:
        current_step, action_hotkey = _failed_spell_logic()
    elif 英雄天赋 == 3:
        if 队伍类型 <= 40:
            # 驱散
            if 纯净术_cd == 0 and dispel_magic_unit is not None and (首领战 in need_dispel_bosses):
                current_step = f"施放 纯净术 on {dispel_magic_unit}"
                action_hotkey = get_hotkey(int(dispel_magic_unit), "纯净术")
            # 愈合祷言
            elif 愈合祷言_cd == 0:
                _mending_filler()
             # 光晕
            elif 施法技能 != 17 and count90 >= 2 and 光晕_cd == 0:
                current_step = "施放 光晕"
                action_hotkey = get_hotkey(0, "光晕")
            elif lowest_u is not None and lowest_p is not None and lowest_p < 治疗限值:
                # 圣言术：静
                if 静_charge <= 3 and lowest_p < 治疗限值 - 10:
                    current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于80%的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                elif 静_cd == 0 and lowest_p < 治疗限值 - 20:
                    current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于60%的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                # 神圣化身
                elif 神圣化身_cd == 0 and 群疗限值数量 >= 3 and 静_cd > 5:
                    current_step = "施放 神圣化身"
                    action_hotkey = get_hotkey(0, "神圣化身")
                # 治疗祷言
                elif 织光层数 > 0 and 圣光涌动 > 0 and 群疗限值数量 >= 3:
                    current_step = "施放 治疗祷言"
                    action_hotkey = get_hotkey(0, "治疗祷言")
                elif 织光层数 > 0 and not 移动 and 施法技能 != 11 and 群疗限值数量 >= 3:
                    current_step = "施放 治疗祷言"
                    action_hotkey = get_hotkey(0, "治疗祷言")
                elif 织光层数 > 0 and not 移动 and 施法技能 == 11 and (群疗限值2数量 > 3 or 群疗限值数量 >= 7):
                    current_step = "施放 治疗祷言"
                    action_hotkey = get_hotkey(0, "治疗祷言")
                # 快速治疗
                elif 织光层数 < 4:
                    current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                else:
                    if 目标有效 and 战斗:
                        _combat_filler()
            elif 目标有效 and 战斗:
                _combat_filler()

        elif 队伍类型 == 46: 
            # 纯净术
            if 纯净术_cd == 0 and dispel_magic_unit is not None and (首领战 not in no_dispel_bosses):
                current_step = f"施放 纯净术 on {dispel_magic_unit}"
                action_hotkey = get_hotkey(int(dispel_magic_unit), "纯净术")
            elif 纯净术_cd == 0 and dispel_unit_disease is not None:
                current_step = f"施放 纯净术 on {dispel_unit_disease}"
                action_hotkey = get_hotkey(int(dispel_unit_disease), "纯净术")
            # 愈合祷言
            elif 愈合祷言_cd == 0:
                _mending_filler()
            # 治疗逻辑
            elif lowest_u is not None and lowest_p is not None and lowest_p < 90:
                # 圣言术：静
                if 静_charge <= 3 and lowest_p < 80:
                    current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于80%的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                elif 静_cd == 0 and lowest_p < 60:
                    current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于60%的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                # 神圣化身
                elif 战斗 and 神圣化身_cd == 0 and count80 >= 3 and 静_cd > 2:
                    current_step = "施放 神圣化身"
                    action_hotkey = get_hotkey(0, "神圣化身")
                # 光晕
                elif 战斗 and count90 >= 3 and 施法技能 != 17 and 光晕_cd == 0:
                    current_step = "施放 光晕"
                    action_hotkey = get_hotkey(0, "光晕")
                # 治疗祷言
                elif 施法技能 != 11 and 织光层数 > 0 and (圣光涌动 > 0 or 织光层数 == 4) and count90 >= 2:
                    current_step = "施放 治疗祷言"
                    action_hotkey = get_hotkey(0, "治疗祷言")
                elif 施法技能 == 11 and 织光层数 > 0 and (圣光涌动 > 0 or 织光层数 == 4) and count80 >= 2:
                    current_step = "施放 治疗祷言"
                    action_hotkey = get_hotkey(0, "治疗祷言")
                # 织光者, 织光层数为0时
                elif 织光层数 == 0:
                    current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                # 快速治疗
                else:
                    current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                
            elif 目标有效 and 战斗:
                _combat_filler()

    return action_hotkey, current_step, unit_info

# 暗影
def _priest_shadow_logic(state_dict):
    spells = state_dict.get("spells") or {}
    生命值 = state_dict.get("生命值")
    一键辅助 = state_dict.get("一键辅助")
    目标有效 = state_dict.get("目标有效")
    战斗 = state_dict.get("战斗")
    引导 = state_dict.get("引导")
    法术失败 = state_dict.get("法术失败", 0)

    action_hotkey = None
    current_step = "无匹配技能"
    unit_info = {}
    action_map = {
        10: ("吸血鬼之触", "吸血鬼之触"),
        2: ("心灵震爆", "心灵震爆"),
        4: ("暗言术：灭", "暗言术：灭"),
        5: ("暗言术：痛", "暗言术：痛"),
        12: ("暗言术：癫", "暗言术：癫"),
        13: ("精神鞭笞", "精神鞭笞"),
        14: ("虚空形态", "虚空形态"),
        15: ("虚空洪流", "虚空洪流"),
        16: ("触须猛击", "触须猛击"),
        17: ("虚空冲击", "虚空冲击"),
        18: ("虚空齐射", "虚空齐射"),
        19: ("精神鞭笞：狂", "精神鞭笞"),
        20: ("光晕", "光晕"),
    }
    if 引导 > 0:
        if 战斗 and 目标有效 and 一键辅助 !=13:
            tup = action_map.get(一键辅助)
            if tup:
                current_step = f"施放 {tup[0]}"
                action_hotkey = get_hotkey(0, tup[1])
            else:
                current_step = "战斗中-无匹配技能"
    elif spells.get("绝望祷言") == 0 and 生命值 < 50:
        current_step = "施放 绝望祷言"
        action_hotkey = get_hotkey(0, "绝望祷言")
    elif 一键辅助 == 1:
        current_step = "施放 真言术：韧"
        action_hotkey = get_hotkey(0, "真言术：韧")
    elif 一键辅助 == 11:
        current_step = "施放 暗影形态"
        action_hotkey = get_hotkey(0, "暗影形态")
    elif 目标有效 and spells.get("虚空形态") < 1 and 法术失败 == 8:
        current_step = "施放 虚空形态"
        action_hotkey = get_hotkey(0, "虚空形态")
    elif spells.get("心灵尖啸") < 1 and 法术失败 == 1:
        current_step = "施放 心灵尖啸"
        action_hotkey = get_hotkey(0, "心灵尖啸")
    elif spells.get("群体驱散") < 1 and 法术失败 == 2:
        current_step = "施放 群体驱散"
        action_hotkey = get_hotkey(0, "群体驱散")
    elif spells.get("吸血鬼的拥抱") < 1 and 法术失败 == 9:
        current_step = "施放 吸血鬼的拥抱"
        action_hotkey = get_hotkey(0, "吸血鬼的拥抱")
    elif 战斗 and 目标有效:
        tup = action_map.get(一键辅助)
        if tup:
            current_step = f"施放 {tup[0]}"
            action_hotkey = get_hotkey(0, tup[1])
        else:
            current_step = "战斗中-无匹配技能"
    return action_hotkey, current_step, unit_info

def run_priest_logic(state_dict, spec_name):
    if spec_name == "戒律":
        return _priest_discipline_logic(state_dict)
    elif spec_name == "神牧":
        return _priest_holy_logic(state_dict)
    elif spec_name == "暗影":
        return _priest_shadow_logic(state_dict)
    return None, "无匹配技能", {}
