local _, fu = ...
if fu.classId ~= 6 then return end
local creat = fu.updateOrCreatTextureByIndex
fu.HarmfulSpellId = 47528

fu.heroSpell = {
    [439843] = 1, -- 死亡使者
    [433901] = 2, -- 萨莱因
    [444005] = 3, -- 天启骑士
}

function fu.updateSpecInfo()
    local specIndex = C_SpecializationInfo.GetSpecialization()
    fu.powerType = nil
    fu.blocks = nil
    fu.group_blocks = nil
    fu.assistant_spells = nil
    if specIndex == 1 then
        fu.blocks = {
            runes = 21,
            ["目标生命值"] = 22,
            ["敌人人数"] = 23,
            spell_cd = {
                [46585] = { index = 31, name = "亡者复生" },
                [55233] = { index = 32, name = "吸血鬼之血" },
                [48792] = { index = 33, name = "冰封之韧" },
                [49039] = { index = 34, name = "巫妖之躯" },
            }
        }
    elseif specIndex == 3 then
        fu.blocks = {
            runes = 21,
            ["目标生命值"] = 22,
            ["敌人人数"] = 23,
            auras = {
                ["次级食尸鬼"] = {
                    index = 25,
                    auraRef = fu.auras["次级食尸鬼"],
                    showKey = "remaining",
                },
                ["食尸鬼层数"] = {
                    index = 26,
                    auraRef = fu.auras["次级食尸鬼"],
                    showKey = "count",
                },
                ["末日突降"] = {
                    index = 27,
                    auraRef = fu.auras["末日突降"],
                    showKey = "remaining",
                },
                ["末日突降层数"] = {
                    index = 28,
                    auraRef = fu.auras["末日突降"],
                    showKey = "count",
                },
                ["黑暗援助"] = {
                    index = 29,
                    auraRef = fu.auras["黑暗援助"],
                    showKey = "remaining",
                },
                ["禁断知识"] = {
                    index = 30,
                    auraRef = fu.auras["禁断知识"],
                    showKey = "remaining",
                },
                ["脓疮毒镰"] = {
                    index = 31,
                    auraRef = fu.auras["脓疮毒镰"],
                    showKey = "remaining",
                },
            },
            spell_cd = {
                [46584] = { index = 41, name = "亡者复生" },
                [42650] = { index = 42, name = "亡者大军" },
                [1247378] = { index = 43, name = "腐化", charge = 46 },
                [1233448] = { index = 44, name = "黑暗突变" },
                [343294] = { index = 45, name = "灵魂收割" },
            },
        }
    end
end

function fu.CreateClassMacro()
    local dynamicSpells = {}
    local staticSpells = {
        [1] = "亡者复生",
        [2] = "亡者大军",
        [3] = "凋零缠绕",
        [4] = "天灾打击",
        [5] = "扩散",
        [6] = "爆发",
        [7] = "脓疮打击",
        [8] = "腐化",
        [9] = "黑暗突变",
        [10] = "灵魂收割",
        [11] = "灵界打击",
        [12] = "心脏打击",
        [13] = "[@player]枯萎凋零",
        [14] = "死神的抚摸",
        [15] = "符文刃舞",
        [16] = "精髓分裂",
        [17] = "血液沸腾",
        [18] = "吸血鬼之血",
        [19] = "冰封之韧",
        [20] = "巫妖之躯",
    }
    fu.CreateMacro(dynamicSpells, staticSpells, _)
end
