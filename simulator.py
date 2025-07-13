import pandas as pd

import math
import numpy as np
# === 公用函數 ===
def safe_int(value, default=0):
    try:
        return int(float(value)) if not pd.isna(value) else default
    except:
        return default

def safe_percentage(value, default=0.0):
    if pd.isna(value) or value is None:
        return default
    try:
        if isinstance(value, str):
            value = value.strip()
            if value.endswith('%'):
                return float(value.rstrip('%')) / 100
            else:
                return float(value)
        return float(value)
    except:
        return default

def distance(unit1, unit2):
    return abs(unit1.row - unit2.row) + abs(unit1.col - unit2.col)
def get_vigor_bonus(moral):
    if moral >= 12:
        return 30
    elif moral >= 8:
        return 20
    elif moral >= 4:
        return 10
    else:
        return 0
def selectTarget(attacker, enemies):
    max_attack_range = attacker.move + attacker.longest_weapon_range
    print(f"{attacker.name} 射程 {max_attack_range}")
    in_range_targets = [
        enemy for enemy in enemies
        if enemy.hp > 0 and distance(attacker, enemy) <= max_attack_range
    ]
    for enemy in enemies:
      print(f"{enemy.name} 距離 {distance(attacker, enemy)}")
    if in_range_targets:
        # 找到可攻擊目標：血量最低者
        target = min(in_range_targets, key=lambda e: e.hp)
        print(f"{target.name} 距離 {distance(attacker, target)}")
        return target, True
    else:
        # 找到距離最近的敵人作為移動目標（不攻擊）
        alive_enemies = [e for e in enemies if e.hp > 0]
        if not alive_enemies:
            return None, False
        nearest = min(alive_enemies, key=lambda e: distance(attacker, e))
        return nearest, False

def move(attacker, target, can_attack):
    def try_move(attacker, target_row, target_col, max_steps):
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        for _ in range(max_steps):
            best_direction = None
            min_distance = float('inf')

            for dr, dc in directions:
                new_r = attacker.row + dr
                new_c = attacker.col + dc

                if not (1 <= new_r <= 7 and 1 <= new_c <= 11):
                    continue

                dist = abs(new_r - target_row) + abs(new_c - target_col)
                if dist < min_distance:
                    min_distance = dist
                    best_direction = (dr, dc)

            if best_direction:
                attacker.row += best_direction[0]
                attacker.col += best_direction[1]

    if not can_attack:
        print(f"{attacker.name} 向最近敵人 {target.name} 移動中")
        try_move(attacker, target.row, target.col, attacker.move)
        return False

    dist = distance(attacker, target)
    if dist <= attacker.move + attacker.max_weapon_range:
        weapon_range = attacker.max_weapon_range
        use_max_weapon = True
        print(f"{attacker.name} 使用最強武裝向 {target.name} 移動至射範 {weapon_range}")
    else:
        weapon_range = attacker.longest_weapon_range
        use_max_weapon = False
        print(f"{attacker.name} 使用最遠武裝向 {target.name} 移動至射範 {weapon_range}")

    desired_distance = weapon_range
    while distance(attacker, target) > desired_distance and attacker.move > 0:
        try_move(attacker, target.row, target.col, 1)
        attacker.move -= 1

    return use_max_weapon

def damageCalculation(attacker, defender, use_max_weapon=True, defense_type="否"):
    if use_max_weapon:
        weapon_stat = attacker.max_weapon_stat
        weapon_power = attacker.max_weapon_power
    else:
        weapon_stat = attacker.longest_weapon_stat
        weapon_power = attacker.longest_weapon_power

    if weapon_stat == "射擊":
        attackerCharacterAtk = attacker.pilot.shooting
    elif weapon_stat == "格鬥":
        attackerCharacterAtk = attacker.pilot.melee
    elif weapon_stat == "覺醒":
        attackerCharacterAtk = attacker.pilot.awakening
    elif weapon_stat == "全":
        attackerCharacterAtk = max(attacker.pilot.shooting, attacker.pilot.melee, attacker.pilot.awakening)
    else:
        attackerCharacterAtk = 0
    print(f"char attack {attackerCharacterAtk}")
    defenderCharacterDef = defender.pilot.defense
    attackerUnitAtk = attacker.atk
    if defense_type == "支援防禦":
      defenderUnitDef = math.floor(defender.defense+defender.pilot.support_defense_mod*defender.base_def)
    else:
      defenderUnitDef = defender.defense
    print(f"char def {defenderCharacterDef}")
    print(f"defender.defense {defender.defense}")
    print(f"defender.base_def {defender.base_def}")
    print(f"char def {defenderUnitDef}")

    characterStatRatio = max(0, attackerCharacterAtk - defenderCharacterDef) / 5000
    unitStatRatio = max(0, math.ceil(attackerUnitAtk / 10.0 - defenderUnitDef / 10.0)) / 5000
    characterSigmoidAdjustment = 1.0 / (math.exp((250 * (defenderCharacterDef - attackerCharacterAtk)) / 100000.0) + 1.0)
    unitSigmoidAdjustment = 1.0 / (math.exp((25 * (defenderUnitDef - attackerUnitAtk)) / 100000.0) + 1.0)

    baseDamage = math.ceil((characterStatRatio + unitStatRatio + characterSigmoidAdjustment + unitSigmoidAdjustment) * weapon_power)
    print(f"baseDamage {baseDamage}")

    attackerCombinedStat = math.ceil((attackerUnitAtk + 2 * attackerCharacterAtk) / 10.0)
    targetCombinedStat = math.ceil((defenderUnitDef + 2 * defenderCharacterDef) / 10.0)

    offenseCorrectionExponent = ((5000 - attackerCombinedStat) * 30) / 100000.0
    defenseCorrectionExponent = ((5000 - targetCombinedStat) * 3) / 100000.0

    offenseDamageComponent = 100.0 / (math.exp(offenseCorrectionExponent) + 1.0)
    defenseMitigationComponent = -40.0 / (math.exp(defenseCorrectionExponent) + 1.0)

    damageCorrection = (offenseDamageComponent + defenseMitigationComponent) * baseDamage
    terrainCorrection = 1.0
    battleDamage = math.ceil((baseDamage + damageCorrection) * terrainCorrection)
    print(f"battleDamage {battleDamage}")

    sumAttackerDamageDealtPercent = (attacker.pilot.damageIncrease+attacker.pilot.conditionalDamageIncrease + attacker.pilot.temporaryDamageIncrease) * 100
    print(f"sumAttackerDamageDealtPercent {sumAttackerDamageDealtPercent}")
    sumAttackerCritDamageDealtPercent = 0
    attackerVigorDamageBonus = get_vigor_bonus(attacker.pilot.moral)
    sumDefenderDamageTakenPercent = (defender.pilot.conditionalDamageDecrease +defender.pilot.temporaryDamageDecrease)  * 100
    print(f"sumDefenderDamageTakenPercent {sumDefenderDamageTakenPercent}")

    totalDamageMultiplierPercent = sumAttackerDamageDealtPercent + sumAttackerCritDamageDealtPercent + attackerVigorDamageBonus - sumDefenderDamageTakenPercent
    print(f"totalDamageMultiplierPercent {totalDamageMultiplierPercent}")
    scaledDamage = math.ceil((totalDamageMultiplierPercent * battleDamage) / 100.0)
    if defense_type == "否":
      defensiveCorrection = 1
    else:
      defensiveCorrection = defender.pilot.defensiveCorrection
    combinedDamage = (battleDamage + scaledDamage) * defensiveCorrection

    criticalCorrectionPercent = 0
    finalDamage = max(0, math.ceil(combinedDamage * ((criticalCorrectionPercent + 100.0) / 100.0)))
    return finalDamage

def printMap(units):
    rows, cols = 7, 11
    cell_width = 6

    # 初始化地圖
    grid = [[' ' * cell_width for _ in range(cols)] for _ in range(rows)]

    for unit in units:
        if unit.hp <= 0:
            continue  # 跳過已擊毀單位
        r, c = unit.row - 1, unit.col - 1  # 轉為 0-based index
        if 0 <= r < rows and 0 <= c < cols:
            name = unit.name.strip()
            display = name[:4] if len(name) > 4 else name
            grid[r][c] = display.center(cell_width)

    # 印出地圖
    print("\n=== 戰場地圖 (row x col) ===")
    for r in range(rows):
        print(f"{r+1:>2} |", end="")
        for cell in grid[r]:
            print(cell, end="")
        print()
    
    # 印出底部欄號
    print("    " + "―" * (cols * cell_width))
    print("     ", end="")
    for c in range(1, cols + 1):
        print(str(c).center(cell_width), end="")
    print("\n")
# === 類別定義 ===

class Pilot:
    def __init__(self, row):
        self.defensiveCorrection = safe_percentage(row.get('防禦減傷(盾牌)'))
        self.melee = safe_int(row.get('格鬥'))
        self.shooting = safe_int(row.get('射撃'))
        self.awakening = safe_int(row.get('覺醒'))
        self.defense = safe_int(row.get('防禦'))
        self.reaction = safe_int(row.get('反應'))
        self.chanceStage = safe_int(row.get('最大行动次数'))
        self.damageIncrease = safe_percentage(row.get('常駐增傷'))
        self.conditionalDamageIncrease  = safe_percentage(row.get('特殊增傷'))
        self.conditionalDamageDecrease = safe_percentage(row.get('特殊減傷'))
        self.support_defense = safe_int(row.get('支援防禦'))
        self.support_defense_mod = safe_percentage(row.get('支援防禦加成'))
        self.support_attack = safe_int(row.get('支援攻擊'))
        self.support_attack_mod = safe_percentage(row.get('支援攻擊加成'))
        self.moral = safe_int(row.get('初始MP'))
        self.ability1 = row.get('精神1', '')
        self.ability2 = row.get('精神2', '')
        self.ability3 = row.get('精神3', '')
        # temporary
        self.temporaryDamageIncrease = 0.0
        self.temporaryDamageDecrease = 0.0

class Unit:
    def __init__(self, row):
        self.name = row.get('單位', '')
        self.position = safe_int(row.get('位置'))
        self.atk = safe_int(row.get('ATK'))
        self.defense = safe_int(row.get('DEF'))
        self.mobility = safe_int(row.get('MOB'))
        self.hp = safe_int(row.get('HP'))
        self.base_atk = math.floor(safe_int(row.get('atk(base)'))*(1+safe_percentage(row.get('突破'))))
        self.base_def = math.floor(safe_int(row.get('def(base)'))*(1+safe_percentage(row.get('突破'))))
        self.base_mob = math.floor(safe_int(row.get('mob(base)'))*(1+safe_percentage(row.get('突破'))))
        self.base_hp = math.floor(safe_int(row.get('hp(base)'))*(1+safe_percentage(row.get('突破'))))
        self.max_weapon_power = safe_int(row.get('最强武裝'))
        self.max_weapon_stat = row.get('最强武裝屬性', '')
        self.max_weapon_type = row.get('最强武裝類型', '')
        self.max_weapon_range = safe_int(row.get('最强武裝射程', ''))
        self.longest_weapon_power = safe_int(row.get('最遠武裝'))
        self.longest_weapon_stat = row.get('最遠武裝屬性', '')
        self.longest_weapon_type = row.get('最遠武裝類型', '')
        self.longest_weapon_range = safe_int(row.get('最遠武裝射程', ''))
        self.move = safe_int(row.get('移動', ''))
        self.resistance_type = row.get('抗性', '')
        self.resistance_percent = safe_percentage(row.get('抗性數值'))
        self.action_order = safe_int(row.get('行動順序'))
        self.pilot = Pilot(row)
        # 新增屬性 (稍後由 Team 指派)
        self.row = None
        self.col = None

class Team:
    def __init__(self, name, unit_rows):
        self.name = name
        self.units = [Unit(row) for row in unit_rows]

        if self.name == "Team A":
            start_positions = [(4, 3), (6, 2), (2, 2), (5, 1), (3, 1)]
        elif self.name == "Team B":
            start_positions = [(4, 9), (6, 10), (2, 10), (5, 11), (3, 11)]
        else:
            start_positions = [(0, 0)] * len(self.units)

        for unit, (r, c) in zip(self.units, start_positions):
            unit.row = r
            unit.col = c

class Battleground:
    def __init__(self, team_a_rows, team_b_rows):
        self.team_a = Team("Team A", team_a_rows)
        self.team_b = Team("Team B", team_b_rows)

# === 戰鬥主流程 ===

def Action(attacker, allies, enemies):
    if attacker.hp <= 0:
        return

    print(f"\n--- {attacker.name} 開始行動 (HP: {attacker.hp}) ---")
    printMap(allies + enemies)

    target, can_attack = selectTarget(attacker, enemies)
    if not target:
        print(f"{attacker.name} 找不到任何目標")
        return

    use_max_weapon = move(attacker, target, can_attack)

    if not can_attack:
        print(f"{attacker.name} 尚無攻擊目標，僅移動接近 {target.name}")
        return

    # === 支援防禦判斷 ===
    potential_defenders = [
        unit for unit in enemies
        if unit.hp > 0 and unit != target
        and unit.pilot.support_defense > 0
        and distance(unit, target) <= unit.move
    ]
    support_defender = None
    for unit in potential_defenders:
        dmg = damageCalculation(attacker, unit, use_max_weapon, "支援防禦")
        if dmg < unit.hp:
            support_defender = unit
            break
    if not support_defender and potential_defenders:
        support_defender = max(potential_defenders, key=lambda u: u.hp)

    if support_defender:
        real_target = support_defender
        defense_type = "支援防禦"
        print(f"{support_defender.name} 對 {target.name} 進行支援防禦")
    else:
        real_target = target
        # === 自我防禦判斷 ===
        can_counter = distance(target, attacker) <= target.longest_weapon_range
        dmg_if_defend = damageCalculation(attacker, target, use_max_weapon, "防禦")
        if dmg_if_defend < target.hp and not can_counter:
            defense_type = "防禦"
        else:
            defense_type = "否"

    # === 支援攻擊選擇 ===
    all_support = [
        unit for unit in allies
        if unit.hp > 0 and unit != attacker
        and unit.pilot.support_attack > 0
        and distance(unit, real_target) <= unit.longest_weapon_range
    ]
    sorted_support = sorted(all_support, key=lambda u: -u.mobility)
    valid_support = []
    hp_check = real_target.hp
    for unit in sorted_support:
        dmg = damageCalculation(unit, real_target, True, defense_type)
        if dmg >= hp_check:
            valid_support.append(unit)
            break
        else:
            valid_support.append(unit)
            hp_check -= dmg

    # === 實際套用支援攻擊與主攻擊 ===
    for unit in valid_support:
        dmg = damageCalculation(unit, real_target, True, defense_type)
        real_target.hp -= dmg
        print(f"{unit.name} 支援攻擊 {real_target.name} 造成 {dmg} 傷害")
        if real_target.hp <= 0:
            print(f"{real_target.name} 被擊毀")
            break

    if real_target.hp > 0:
        dmg = damageCalculation(attacker, real_target, use_max_weapon, defense_type)
        real_target.hp -= dmg
        print(f"{attacker.name} 攻擊 {real_target.name} 造成 {dmg} 傷害")
        if real_target.hp <= 0:
            print(f"{real_target.name} 被擊毀")

    initial_target_dead = target.hp <= 0
    printMap(allies + enemies)

    # === 反擊階段 ===
    if not initial_target_dead:
        counter_defense_type = "否"
        counter_support = [
            unit for unit in enemies
            if unit.hp > 0 and unit != target
            and unit.pilot.support_attack > 0
            and distance(unit, attacker) <= unit.longest_weapon_range
        ]
        sorted_counter = sorted(counter_support, key=lambda u: -u.mobility)
        valid_counter = []
        atk_hp_check = attacker.hp
        for unit in sorted_counter:
            dmg = damageCalculation(unit, attacker, True, counter_defense_type)
            if dmg >= atk_hp_check:
                valid_counter.append(unit)
                break
            else:
                valid_counter.append(unit)
                atk_hp_check -= dmg

        for unit in valid_counter:
            dmg = damageCalculation(unit, attacker, True, counter_defense_type)
            attacker.hp -= dmg
            print(f"{unit.name} 支援反擊 {attacker.name} 造成 {dmg} 傷害")
            if attacker.hp <= 0:
                print(f"{attacker.name} 被擊毀")
                break

        if attacker.hp > 0:
            dmg = damageCalculation(target, attacker, True, counter_defense_type)
            attacker.hp -= dmg
            print(f"{target.name} 反擊 {attacker.name} 造成 {dmg} 傷害")
            if attacker.hp <= 0:
                print(f"{attacker.name} 被擊毀")

    printMap(allies + enemies)

    if attacker.hp > 0 and initial_target_dead and attacker.pilot.chanceStage > 0:
        attacker.pilot.chanceStage -= 1
        print(f"{attacker.name} 擊破敵人，剩餘行動次數 {attacker.pilot.chanceStage}")
        Action(attacker, allies, enemies)

# === 讀取 Google Sheet ===

SHEET_ID = '1rf1uZHKJhhCQ_10qvzQkoSaD56ExFxE8SOWAxjXlwyo'
GID = '489835885'
CSV_URL = f'https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv&gid={GID}'

df = pd.read_csv(CSV_URL, header=2)
df.dropna(axis=1, how='all', inplace=True)

# 擷取雙方隊伍
team_a_rows = [row for _, row in df.iloc[0:5].iterrows()]
team_b_rows = [row for _, row in df.iloc[9:14].iterrows()]
battleground = Battleground(team_a_rows, team_b_rows)

# 依行動順序執行
all_units = battleground.team_a.units + battleground.team_b.units
sorted_units = sorted([u for u in all_units if u.hp > 0], key=lambda u: u.action_order)
attacker = battleground.team_a.units[3]
# 執行所有行動
for unit in sorted_units:
    allies = battleground.team_a.units if unit in battleground.team_a.units else battleground.team_b.units
    enemies = battleground.team_b.units if unit in battleground.team_a.units else battleground.team_a.units
    Action(unit, allies, enemies)