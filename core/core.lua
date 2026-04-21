local _, fu = ...


-- 游戏内宏命令
-- /fu 命令系统
-- /fu switch   — AOE / 单体 切换 (Block 50)
-- /fu aoe      — 仅开 AOE 模式
-- /fu single   — 仅开 单体 模式
-- /fu cd       — 爆发 开 / 关 切换 (Block 51)
--

local mode = 0
local cooldowns = 0

local function switchCooldown()
    if cooldowns == 0 then
        print("|cff00ff00[Fuyutsui]|r 爆发已|cffff0000关闭|r") -- 修改"关闭"为红色
    else
        print("|cff00ff00[Fuyutsui]|r 爆发已|cff00ff00开启|r")
    end
    if fu.blocks and fu.blocks["爆发开关"] then
        fu.updateOrCreatTextureByIndex(fu.blocks["爆发开关"], cooldowns / 255)
    end
end

local function switchMode()
    if mode == 0 then
        print("|cff00ff00[Fuyutsui]|r 已切换|cff00ff00默认|r模式！")
    elseif mode == 1 then
        print("|cff00ff00[Fuyutsui]|r 已切换|cff00ff00单体|r模式！")
    elseif mode == 2 then
        print("|cff00ff00[Fuyutsui]|r 已切换|cff00ff00AOE|r模式！")
    end
    if fu.blocks and fu.blocks["AOE开关"] then
        fu.updateOrCreatTextureByIndex(fu.blocks["AOE开关"], mode / 255)
    end
end

-- 定义主处理函数
local function Fuyutsui_SlashHandler(msg)
    -- 将输入转换为小写并拆分参数
    local command = string.lower(msg:trim())

    if command == "switch" then
        mode = (mode + 1) % 3
        switchMode()
    elseif command == "default" then
        mode = 0
        switchMode()
    elseif command == "aoe" then
        mode = 2
        switchMode()
    elseif command == "single" then
        mode = 1
        switchMode()
    elseif command == "cd" then
        cooldowns = (cooldowns == 0) and 1 or 0
        switchCooldown()
    else
        -- 默认显示的帮助信息
        print("|cff00ff00Fuyutsui|r 命令列表:")
        print("/fu switch - 切换模式")
        print("/fu aoe - AOE模式")
        print("/fu single - 单体模式")
        print("/fu cd - 冷却检查")
    end
end

-- 绑定命令（使用你定义的变量名）
SLASH_FUYUTSUI1 = "/fu"
SLASH_FUYUTSUI2 = "/fuyutsui"
SlashCmdList["FUYUTSUI"] = Fuyutsui_SlashHandler

function SetTestSecret(set)
    SetCVar("secretChallengeModeRestrictionsForced", set)
    SetCVar("secretCombatRestrictionsForced", set)
    SetCVar("secretEncounterRestrictionsForced", set)
    SetCVar("secretMapRestrictionsForced", set)
    SetCVar("secretPvPMatchRestrictionsForced", set)
    SetCVar("secretAuraDataRestrictionsForced", set)
    SetCVar("scriptErrors", set);
    SetCVar("doNotFlashLowHealthWarning", set);
end

-- /script SetTestSecret(0)
SetTestSecret(1)

---@param reversed boolean 是否逆序
---@param forceParty boolean 是否强制使用队伍
---@return function 迭代器
function fu.IterateGroupMembers(reversed, forceParty)
    local unit = (not forceParty and IsInRaid()) and 'raid' or 'party'
    local numGroupMembers = unit == 'party' and GetNumSubgroupMembers() or GetNumGroupMembers()
    local i = reversed and numGroupMembers or (unit == 'party' and 0 or 1)
    return function()
        local ret
        if i == 0 and unit == 'party' then
            ret = 'player'
        elseif i <= numGroupMembers and i > 0 then
            ret = unit .. i
        end
        i = i + (reversed and -1 or 1)
        return ret
    end
end

function fu.creatColorCurve(point, b)
    local curve = C_CurveUtil.CreateColorCurve()
    curve:SetType(Enum.LuaCurveType.Linear)
    curve:AddPoint(0, CreateColor(0, 0, 0, 1))
    curve:AddPoint(point, CreateColor(0, 0, b / 255, 1))
    return curve
end
