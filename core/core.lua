local _, fu = ...


-- 游戏内宏命令
-- /fu 命令系统
-- /fu cd       — 爆发 开 / 关 切换 (Block 51)

-- /fu aoemode   — 默认 / AOE / 单体 切换 (Block 50)
-- /fu aoemode default  — 切换回默认模式
-- /fu aoemode aoe      — 仅开 AOE 模式
-- /fu aoemode single   — 仅开 单体 模式

-- /fu dpsmode  — DPS 模式 开 / 关 切换 (Block 52)
-- /fu dpsmode manual     — 输出模式 切换到 手动编写逻辑
-- /fu dpsmode assistant  — 输出模式 切换到 官方一键辅助

local aoeMode = 0
local cooldowns = 0
local dpsMode = 0

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

local function switchAoeMode()
    if aoeMode == 0 then
        print("|cff00ff00[Fuyutsui]|r 已切换|cff00ff00自动|r模式！")
    elseif aoeMode == 1 then
        print("|cff00ff00[Fuyutsui]|r 已切换|cff00ff00单体|r模式！")
    end
    if fu.blocks and fu.blocks["AOE开关"] then
        fu.updateOrCreatTextureByIndex(fu.blocks["AOE开关"], aoeMode / 255)
    end
end

local function switchDpsMode()
    if dpsMode == 0 then
        print("|cff00ff00[Fuyutsui]|r 输出模式已修改为|cff00ff00官方一键辅助|r") -- 修改"关闭"为红色
    else
        print("|cff00ff00[Fuyutsui]|r 输出模式已修改为|cff00ff00手动编写逻辑|r")
    end
    if fu.blocks and fu.blocks["输出模式"] then
        fu.updateOrCreatTextureByIndex(fu.blocks["输出模式"], dpsMode / 255)
    end
end

-- 定义主处理函数
local function Fuyutsui_SlashHandler(msg)
    -- 将输入转换为小写并拆分参数
    local command = string.lower(msg:trim())
    -- 爆发
    if command == "cd" then
        cooldowns = (cooldowns == 0) and 1 or 0
        switchCooldown()
        -- AOE模式
    elseif command == "aoemode" then
        aoeMode = (aoeMode == 0) and 1 or 0
        switchAoeMode()
    elseif command == "aoemode auto" or command == "aoemode aoe" then
        aoeMode = 0
        switchAoeMode()
    elseif command == "aoemode single" then
        aoeMode = 1
        switchAoeMode()
        -- 输出模式
    elseif command == "dpsmode" then
        dpsMode = (dpsMode == 0) and 1 or 0
        switchDpsMode()
    elseif command == "dpsmode manual" then
        dpsMode = 1
        switchDpsMode()
    elseif command == "dpsmode assistant" then
        dpsMode = 0
        switchDpsMode()
    else
        -- 默认显示的帮助信息
        print("|cff00ff00Fuyutsui|r 命令列表:")
        print("/fu cd                   - 冷却检查")
        print("/fu aoemode              - 切换模式")
        print("/fu aoemode auto         - 自动模式 (根据插件推荐)")
        print("/fu aoemode single       - 单体模式 (强制单体)")
        print("/fu dpsmode              - 输出模式切换")
        print("/fu dpsmode manual       - 手动编写逻辑")
        print("/fu dpsmode assistant    - 官方一键辅助")
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
    print("|cff00ff00[Fuyutsui]|r 已设置测试模式: " .. (set == 1 and "|cff00ff00开启|r" or "|cffff0000关闭|r"))
end

-- /script SetTestSecret(0)
SetTestSecret(1)

function FuGetAuraDate(unit)
    for i = 1, 40 do
        local aura = C_UnitAuras.GetAuraDataByIndex(unit, i)
        if aura then
            for key, value in pairs(aura) do
                if key == "name" then
                    print(value, issecretvalue(key), issecretvalue(value))
                end
            end
        end
    end
end

-- /script FuGetAuraDate("player", id)

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
