# -*- coding: utf-8 -*-
"""牧师职业的逻辑决策（戒律 / 暗影）。"""

from utils import *

def run_priest_logic(state_dict, spec_name):
    spells = state_dict.get("spells") or {}
    health = state_dict.get("生命值")
    power = state_dict.get("能量值")
    assistant = state_dict.get("一键辅助")
    target_valid = state_dict.get("目标有效")
    combat = state_dict.get("战斗")
    casting = state_dict.get("施法")
    channeling = state_dict.get("引导")
    moving = state_dict.get("移动")
    group_type = int(state_dict.get("队伍类型", 0) or 0)
    hero_talent = int(state_dict.get("英雄天赋", 0) or 0)
    boss_id = int(state_dict.get("首领战", 0) or 0)
    # 默认返回：无操作
    action_hotkey = None
    current_step = "无匹配技能"
    unit_info = {}

    if spec_name == "戒律":
        evangelism_cd = spells.get("福音", -1)
        radiance_cd = spells.get("真言术：耀", -1)
        shield_cd = spells.get("真言术：盾", -1)
        penance_cd = spells.get("苦修", -1)
        shadow_death_cd = spells.get("暗言术：灭", -1)
        mind_blast_cd = spells.get("心灵震爆", -1)
        entropic_rift_cd = state_dict.get("熵能裂隙", 0)
        surge_of_light = state_dict.get("圣光涌动", 0)
        void_shield = state_dict.get("虚空之盾", -1)
        evangelism_buff = state_dict.get("福音", 0)

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

        if channeling > 0:
            current_step = "引导,不执行任何操作"
        elif spells.get("绝望祷言") == 0 and health < 50:
            current_step = "施放 绝望祷言"
            action_hotkey = get_hotkey(0, "绝望祷言")
        elif spells.get("奥术洪流") == 0 and power <= 90:
            current_step = "施放 奥术洪流"
            action_hotkey = get_hotkey(0, "奥术洪流")
        elif assistant == 5:
            current_step = "施放 真言术：韧"
            action_hotkey = get_hotkey(0, "真言术：韧")
        elif spells.get("心灵尖啸") < 1 and state_dict.get("法术失败") == 32:
            current_step = "施放 心灵尖啸"
            action_hotkey = get_hotkey(0, "心灵尖啸")
        elif spells.get("群体驱散") < 1 and state_dict.get("法术失败") == 33:
            current_step = "施放 群体驱散"
            action_hotkey = get_hotkey(0, "群体驱散")
        elif spells.get("真言术：障") < 1 and state_dict.get("法术失败") == 34:
            current_step = "施放 真言术：障"
            action_hotkey = get_hotkey(0, "真言术：障")
        elif spells.get("终极苦修") < 1 and state_dict.get("法术失败") == 35:
            current_step = "施放 终极苦修"
            action_hotkey = get_hotkey(0, "终极苦修")
        elif hero_talent == 1:
            if group_type <= 40:
                if evangelism_cd == 0 and no_ato_count_90 >= 4:
                    current_step = "施放 福音"
                    action_hotkey = get_hotkey(0, "福音")
                elif radiance_cd == 0 and no_ato_count_90 >= 4 and evangelism_buff > 0:
                    current_step = "施放 真言术：耀"
                    action_hotkey = get_hotkey(0, "真言术：耀")
                elif target_valid and combat and assistant == 4:
                    current_step = "施放 暗言术：痛"
                    action_hotkey = get_hotkey(0, "暗言术：痛")
                elif surge_of_light > 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                    current_step = f"施放 快速治疗 on {no_ato_u}, 无救赎生命低于90%的单位"
                    action_hotkey = get_hotkey(int(no_ato_u), "快速治疗")
                elif surge_of_light > 0 and lowest_u is not None and lowest_p is not None and lowest_p < 70:
                    current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                elif shield_cd == 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                    current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎单位"
                    action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")
                elif shield_cd == 0 and no_shd_lowest_u is not None and no_shd_lowest_p is not None and no_shd_lowest_p < 90:
                    current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                    action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
                elif shield_cd == 0 and no_shd_tank is not None:
                    current_step = f"施放 真言术：盾 on {no_shd_tank}, 无盾单位"
                    action_hotkey = get_hotkey(int(no_shd_tank), "真言术：盾")
                elif shield_cd == 0 and no_shd_lowest_u is not None:
                    current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                    action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
                elif radiance_cd == 0 and casting == 0 and no_ato_count_90 >= 5:
                    current_step = "施放 真言术：耀"
                    action_hotkey = get_hotkey(0, "真言术：耀")
                elif penance_cd == 0 and lowest_u is not None and lowest_p is not None and lowest_p < 75:
                    current_step = f"施放 苦修 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "苦修")
                elif target_valid and combat:
                    if shadow_death_cd == 0:
                        current_step = "施放 暗言术：灭"
                        action_hotkey = get_hotkey(0, "暗言术：灭")
                    elif not moving and mind_blast_cd == 0:
                        current_step = "施放 心灵震爆"
                        action_hotkey = get_hotkey(0, "心灵震爆")
                    elif penance_cd == 0:
                        current_step = "施放 苦修"
                        action_hotkey = get_hotkey(0, "苦修")
                    elif not moving:
                        current_step = "施放 惩击"
                        action_hotkey = get_hotkey(0, "惩击")
                    else:
                        current_step = "战斗中-无匹配技能"
            elif group_type == 46:
                if spells.get("纯净术") == 0 and dispel_unit is not None:
                    current_step = f"施放 纯净术 on {dispel_unit}"
                    action_hotkey = get_hotkey(int(dispel_unit), "纯净术")
                elif evangelism_cd == 0 and no_ato_count_90 >= 4:
                    current_step = "施放 福音"
                    action_hotkey = get_hotkey(0, "福音")
                elif radiance_cd == 0 and no_ato_count_90 >= 4 and evangelism_buff > 0:
                    current_step = "施放 真言术：耀"
                    action_hotkey = get_hotkey(0, "真言术：耀")
                elif target_valid and combat and assistant == 4:
                    current_step = "施放 暗言术：痛"
                    action_hotkey = get_hotkey(0, "暗言术：痛")
                elif surge_of_light > 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                    current_step = f"施放 快速治疗 on {no_ato_u}, 无救赎生命低于90%的单位"
                    action_hotkey = get_hotkey(int(no_ato_u), "快速治疗")
                elif surge_of_light > 0 and lowest_u is not None and lowest_p is not None and lowest_p < 70:
                    current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                elif shield_cd == 0 and no_ato_u is not None and no_ato_p is not None and no_ato_p < 90:
                    current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎单位"
                    action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")
                elif shield_cd == 0 and no_shd_lowest_u is not None and no_shd_lowest_p is not None and no_shd_lowest_p < 90:
                    current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                    action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
                elif shield_cd == 0 and no_shd_tank is not None:
                    current_step = f"施放 真言术：盾 on {no_shd_tank}, 无盾单位"
                    action_hotkey = get_hotkey(int(no_shd_tank), "真言术：盾")
                elif shield_cd == 0 and no_shd_lowest_u is not None:
                    current_step = f"施放 真言术：盾 on {no_shd_lowest_u}, 无盾生命最低的单位"
                    action_hotkey = get_hotkey(int(no_shd_lowest_u), "真言术：盾")
                elif radiance_cd == 0 and casting == 0 and no_ato_count_90 >= 5:
                    current_step = "施放 真言术：耀"
                    action_hotkey = get_hotkey(0, "真言术：耀")
                elif penance_cd == 0 and lowest_u is not None and lowest_p is not None and lowest_p < 75:
                    current_step = f"施放 苦修 on {lowest_u}, 生命最低的单位"
                    action_hotkey = get_hotkey(int(lowest_u), "苦修")
                elif target_valid and combat:
                    if shadow_death_cd == 0:
                        current_step = "施放 暗言术：灭"
                        action_hotkey = get_hotkey(0, "暗言术：灭")
                    elif not moving and mind_blast_cd == 0:
                        current_step = "施放 心灵震爆"
                        action_hotkey = get_hotkey(0, "心灵震爆")
                    elif penance_cd == 0:
                        current_step = "施放 苦修"
                        action_hotkey = get_hotkey(0, "苦修")
                    elif not moving:
                        current_step = "施放 惩击"
                        action_hotkey = get_hotkey(0, "惩击")
                    else:
                        current_step = "战斗中-无匹配技能"

        elif hero_talent == 2:
            if combat:
                if target_valid and assistant == 4:
                    current_step = "施放 暗言术：痛"
                    action_hotkey = get_hotkey(0, "暗言术：痛")
                elif target_valid and entropic_rift_cd > 0 and penance_cd == 0:
                    current_step = "施放 苦修"
                    action_hotkey = get_hotkey(0, "苦修")
                elif shield_cd == 0  and no_ato_u is not None and no_ato_p < 99:
                    current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎生命最低的单位, 有虚空之盾"
                    action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")
                elif surge_of_light > 0 and no_ato_u is not None and no_ato_p < 90:
                    current_step = f"施放 快速治疗 on {no_ato_u}, 无救赎生命低于90%的单位"
                    action_hotkey = get_hotkey(int(no_ato_u), "快速治疗")
                elif evangelism_cd == 0 and (no_ato_count_90 >= 4 or (group_type == 46 and no_ato_count_90 >= 1)):
                    current_step = "施放 福音"
                    action_hotkey = get_hotkey(0, "福音")
                elif radiance_cd == 0 and casting == 0 and (no_ato_count_90 >= 4 or (group_type == 46 and no_ato_count_90 >= 1)):
                    current_step = "施放 真言术：耀"
                    action_hotkey = get_hotkey(0, "真言术：耀")
                elif shadow_death_cd == 0:
                    current_step = "施放 暗言术：灭"
                    action_hotkey = get_hotkey(0, "暗言术：灭")
                elif not moving and mind_blast_cd == 0:
                    current_step = "施放 心灵震爆"
                    action_hotkey = get_hotkey(0, "心灵震爆")
                elif not moving and target_valid and entropic_rift_cd > 0:
                    current_step = "施放 惩击"
                    action_hotkey = get_hotkey(0, "惩击")
                elif shield_cd == 0 and no_ato_u is not None and no_ato_p < 90:
                    current_step = f"施放 真言术：盾 on {no_ato_u}, 无救赎生命最低的单位"
                    action_hotkey = get_hotkey(int(no_ato_u), "真言术：盾")   
                elif target_valid and penance_cd == 0 and void_shield == 0:
                    current_step = "施放 苦修"
                    action_hotkey = get_hotkey(0, "苦修")
                elif target_valid:
                    current_step = "施放 惩击"
                    action_hotkey = get_hotkey(0, "惩击")

    elif spec_name == "神牧":
        mending_cd = spells.get("愈合祷言", -1)
        serenity_cd = spells.get("圣言术：静", -1)
        serenity_charge = spells.get("静充能", -1)
        chastise_cd = spells.get("圣言术：罚", -1)
        purify_cd = spells.get("纯净术", -1)
        desperate_cd = spells.get("绝望祷言", -1)
        holy_fire_cd = spells.get("神圣之火", -1)
        divine_hymn_cd = spells.get("神圣赞美诗", -1)
        halo_cd = spells.get("光晕", -1)
        apotheosis_cd = spells.get("神圣化身", -1)

        lightweaver = state_dict.get("织光者", 0)
        lightweaver_count = state_dict.get("织光层数", 0)
        light_burst = state_dict.get("圣光涌动", 0)
        benediction = state_dict.get("祈福", 0)
        casting_spell = state_dict.get("施法技能", 0)

        dispel_unit, _ = get_unit_with_dispel_type(state_dict, 1)
        lowest_u, lowest_p = get_lowest_health_unit(state_dict, 100)
        no_mend_u, no_mend_p = get_lowest_health_unit_without_aura(state_dict, "愈合祷言", 101)
        no_mend_tank, no_mend_tank_pct = get_unit_with_role_and_without_aura_name(state_dict, 1, "愈合祷言")
        count90 = get_count_units_below_health(state_dict, 90)
        count80 = get_count_units_below_health(state_dict, 80)

        if casting_spell == 11 and lightweaver_count > 0:
            lightweaver_count = lightweaver_count - 1
        if casting_spell == 4 or casting_spell == 19:
            lightweaver_count = lightweaver_count + 1

        if channeling > 0:
            current_step = "引导,不执行任何操作"
        elif desperate_cd == 0 and health < 50:
            current_step = "施放 绝望祷言"
            action_hotkey = get_hotkey(0, "绝望祷言")
        elif spells.get("奥术洪流") == 0 and power <= 90:
            current_step = "施放 奥术洪流"
            action_hotkey = get_hotkey(0, "奥术洪流")
        elif assistant == 5:
            current_step = "施放 真言术：韧"
            action_hotkey = get_hotkey(0, "真言术：韧")
        elif spells.get("心灵尖啸") < 1 and state_dict.get("法术失败") == 33:
            current_step = "施放 心灵尖啸"
            action_hotkey = get_hotkey(0, "心灵尖啸")
        elif spells.get("群体驱散") < 1 and state_dict.get("法术失败") == 34:
            current_step = "施放 群体驱散"
            action_hotkey = get_hotkey(0, "群体驱散")
        elif divine_hymn_cd == 0 and state_dict.get("法术失败") == 31:
            current_step = "施放 神圣赞美诗"
            action_hotkey = get_hotkey(0, "神圣赞美诗")
        elif halo_cd == 0 and state_dict.get("法术失败") == 30:
            current_step = "施放 光晕"
            action_hotkey = get_hotkey(0, "光晕")
        elif apotheosis_cd == 0 and state_dict.get("法术失败") == 29:
            current_step = "施放 神圣化身"
            action_hotkey = get_hotkey(0, "神圣化身")
        elif hero_talent == 3:
            if group_type <= 40:
                if purify_cd == 0 and dispel_unit is not None and (boss_id == 4 or boss_id == 5):
                    current_step = f"施放 纯净术 on {dispel_unit}"
                    action_hotkey = get_hotkey(int(dispel_unit), "纯净术")
                # 愈合祷言
                elif mending_cd == 0 and no_mend_u is not None and no_mend_p is not None and no_mend_p < 95:
                    current_step = f"施放 愈合祷言 on {no_mend_u}, 无愈合祷言生命低于95%的单位"
                    action_hotkey = get_hotkey(int(no_mend_u), "愈合祷言")
                elif mending_cd == 0 and no_mend_tank is not None:
                    current_step = f"施放 愈合祷言 on {no_mend_tank}, 无愈合祷言坦克"
                    action_hotkey = get_hotkey(int(no_mend_tank), "愈合祷言")
                elif mending_cd == 0 and no_mend_u is not None:
                    current_step = f"施放 愈合祷言 on {no_mend_u}, 无愈合祷言的单位"
                    action_hotkey = get_hotkey(int(no_mend_u), "愈合祷言")
                elif lowest_u is not None and lowest_p is not None and lowest_p < 90:
                    # 圣言术：静
                    if serenity_charge <= 3 and lowest_p < 85:
                        current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于80%的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                    elif serenity_cd == 0 and lowest_p < 60:
                        current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于60%的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                    # 神圣化身
                    elif apotheosis_cd == 0 and count80 >= 4 and serenity_cd > 5:
                        current_step = "施放 神圣化身"
                        action_hotkey = get_hotkey(0, "神圣化身")
                    # 光晕
                    elif count90 >= 4 and halo_cd == 0:
                        current_step = "施放 光晕"
                        action_hotkey = get_hotkey(0, "光晕")
                    # 织光者, 织光层数为0时
                    elif lightweaver_count == 0 or (benediction > 0 and lowest_p < 80) :
                        current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                    # 治疗祷言
                    elif lightweaver_count > 0 and light_burst > 0 and count90 >= 3:
                        current_step = "施放 治疗祷言"
                        action_hotkey = get_hotkey(0, "治疗祷言")
                    elif not moving and lightweaver_count == 4 and count90 >= 5:
                        current_step = "施放 治疗祷言"
                        action_hotkey = get_hotkey(0, "治疗祷言")
                    elif not moving and lightweaver_count > 0 and count80 >= 5:
                        current_step = "施放 治疗祷言"
                        action_hotkey = get_hotkey(0, "治疗祷言")
                    # 快速治疗
                    elif lightweaver_count < 3 and lowest_p < 80:
                        current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                    elif lowest_p < 70:
                        current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                    elif target_valid and combat:
                        if not moving and holy_fire_cd == 0:
                            current_step = "施放 神圣之火"
                            action_hotkey = get_hotkey(0, "神圣之火")
                        elif not moving:
                            current_step = "施放 惩击"
                            action_hotkey = get_hotkey(0, "惩击")
                        else:
                            current_step = "战斗中-无匹配技能"
            elif group_type == 46:
                if purify_cd == 0 and dispel_unit is not None:
                    current_step = f"施放 纯净术 on {dispel_unit}"
                    action_hotkey = get_hotkey(int(dispel_unit), "纯净术")
                # 愈合祷言
                elif mending_cd == 0 and no_mend_u is not None and no_mend_p is not None and no_mend_p < 95:
                    current_step = f"施放 愈合祷言 on {no_mend_u}, 无愈合祷言生命低于95%的单位"
                    action_hotkey = get_hotkey(int(no_mend_u), "愈合祷言")
                elif mending_cd == 0 and no_mend_tank is not None:
                    current_step = f"施放 愈合祷言 on {no_mend_tank}, 无愈合祷言坦克"
                    action_hotkey = get_hotkey(int(no_mend_tank), "愈合祷言")
                elif mending_cd == 0 and no_mend_u is not None:
                    current_step = f"施放 愈合祷言 on {no_mend_u}, 无愈合祷言的单位"
                    action_hotkey = get_hotkey(int(no_mend_u), "愈合祷言")
                elif lowest_u is not None and lowest_p is not None and lowest_p < 90:
                    # 圣言术：静
                    if serenity_charge <= 3 and lowest_p < 80:
                        current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于80%的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                    elif serenity_cd == 0 and lowest_p < 60:
                        current_step = f"施放 圣言术：静 on {lowest_u}, 生命低于60%的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "圣言术：静")
                    # 神圣化身
                    elif combat and apotheosis_cd == 0 and count80 >= 3 and serenity_cd > 5:
                        current_step = "施放 神圣化身"
                        action_hotkey = get_hotkey(0, "神圣化身")
                    # 光晕
                    elif combat and count90 >= 3 and halo_cd == 0:
                        current_step = "施放 光晕"
                        action_hotkey = get_hotkey(0, "光晕")
                    # 治疗祷言
                    elif lightweaver_count > 0 and (light_burst > 0 or lightweaver_count == 4) and count90 >= 2:
                        current_step = "施放 治疗祷言"
                        action_hotkey = get_hotkey(0, "治疗祷言")
                    # 祈福
                    elif benediction > 0:
                        current_step = f"祈福 施放 快速治疗 on {lowest_u}, 生命最低的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                    # 织光者, 织光层数为0时
                    elif lightweaver_count == 0:
                        current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                    # 治疗祷言
                    elif lightweaver_count > 0 and (light_burst > 0 or lightweaver_count == 4) and count90 >= 2:
                        current_step = "施放 治疗祷言"
                        action_hotkey = get_hotkey(0, "治疗祷言")
                    elif lightweaver_count > 0 and count80 >= 2:
                        current_step = "施放 治疗祷言"
                        action_hotkey = get_hotkey(0, "治疗祷言")
                    # 快速治疗
                    else:
                        current_step = f"施放 快速治疗 on {lowest_u}, 生命最低的单位"
                        action_hotkey = get_hotkey(int(lowest_u), "快速治疗")
                elif target_valid and combat:
                    if not moving and holy_fire_cd == 0:
                        current_step = "施放 神圣之火"
                        action_hotkey = get_hotkey(0, "神圣之火")
                    elif not moving:
                        current_step = "施放 惩击"
                        action_hotkey = get_hotkey(0, "惩击")
                    else:
                        current_step = "战斗中-无匹配技能"

    elif spec_name == "暗影":
        # 暗影逻辑比较简单，不需要 unit_info
        if channeling > 0:
            if combat and target_valid and assistant !=8:
                action_map = {
                    1: ("吸血鬼之触", "吸血鬼之触"),
                    2: ("心灵震爆", "心灵震爆"),
                    4: ("暗言术：灭", "暗言术：灭"),
                    5: ("暗言术：痛", "暗言术：痛"),
                    6: ("暗言术：癫", "暗言术：癫"),
                    8: ("精神鞭笞", "精神鞭笞"),
                    9: ("虚空形态", "虚空形态"),
                    10: ("虚空洪流", "虚空洪流"),
                    11: ("触须猛击", "触须猛击"),
                    12: ("虚空冲击", "虚空冲击"),
                    13: ("虚空齐射", "虚空齐射"),
                    14: ("精神鞭笞：狂", "精神鞭笞"),
                    15: ("光晕", "光晕"),
                }
                tup = action_map.get(assistant)
                if tup:
                    current_step = f"施放 {tup[0]}"
                    action_hotkey = get_hotkey(0, tup[1])
                else:
                    current_step = "战斗中-无匹配技能"
        elif spells.get("绝望祷言") == 0 and health < 50:
            current_step = "施放 绝望祷言"
            action_hotkey = get_hotkey(0, "绝望祷言")
        elif assistant == 7:
            current_step = "施放 真言术：韧"
            action_hotkey = get_hotkey(0, "真言术：韧")
        elif assistant == 3:
            current_step = "施放 暗影形态"
            action_hotkey = get_hotkey(0, "暗影形态")
        elif target_valid and spells.get("虚空形态") < 1 and state_dict.get("法术失败") == 34:
            current_step = "施放 虚空形态"
            action_hotkey = get_hotkey(0, "虚空形态")
        elif spells.get("心灵尖啸") < 1 and state_dict.get("法术失败") == 37:
            current_step = "施放 心灵尖啸"
            action_hotkey = get_hotkey(0, "心灵尖啸")
        elif spells.get("群体驱散") < 1 and state_dict.get("法术失败") == 38:
            current_step = "施放 群体驱散"
            action_hotkey = get_hotkey(0, "群体驱散")
        elif spells.get("吸血鬼的拥抱") < 1 and state_dict.get("法术失败") == 39:
            current_step = "施放 吸血鬼的拥抱"
            action_hotkey = get_hotkey(0, "吸血鬼的拥抱")
        elif combat and target_valid:
            action_map = {
                1: ("吸血鬼之触", "吸血鬼之触"),
                2: ("心灵震爆", "心灵震爆"),
                4: ("暗言术：灭", "暗言术：灭"),
                5: ("暗言术：痛", "暗言术：痛"),
                6: ("暗言术：癫", "暗言术：癫"),
                8: ("精神鞭笞", "精神鞭笞"),
                9: ("虚空形态", "虚空形态"),
                10: ("虚空洪流", "虚空洪流"),
                11: ("触须猛击", "触须猛击"),
                12: ("虚空冲击", "虚空冲击"),
                13: ("虚空齐射", "虚空齐射"),
                14: ("精神鞭笞：狂", "精神鞭笞"),
                15: ("光晕", "光晕"),
            }
            tup = action_map.get(assistant)
            if tup:
                current_step = f"施放 {tup[0]}"
                action_hotkey = get_hotkey(0, tup[1])
            else:
                current_step = "战斗中-无匹配技能"

    

    return action_hotkey, current_step, unit_info
