import math
import sys

# https://www.codingame.com/ide/challenge/spring-challenge-2022

# Default positions for defenders improve a little (more to the border maybe?)
# TODO: Marcin: Refactor to 'STANCES' so that I can dynamically change behavior

# Improve defenders, probably should take into account enemy attacker position, at least for one of defenders
# Looks like this is the biggest bottleneck at the moment

# Wind -> Shield combo more efficient
# Control of enemy hero if score guaranteed

# TODO: Marcin: Control -> Shield for enemies close to base


# At least one defender should prio defense over control
# TODO: Marcin: Well, now defenders are too aggresive with control
# TODO: Marcin: Add 'wandering mode' if nothing to do

# MORE 'states' e.g. if there are many enemies in enemy base then 'dive mode'

# TODO: Marcin: Simulate if it's better to use wind or just hit to death (rist that enemy will wind it into my base)
# TODO: Handle fog of war

MAX_X = 17_630
MAX_Y = 9_000

BASE_X, BASE_Y = [int(i) for i in input().split()]
HEROES_PER_PLAYER = int(input())

HERO_TYPE_ATTACKER = "ATTACKER"
HERO_TYPE_DEFENDER = "DEFENDER"


def transpose(point):
    return abs(BASE_X - point[0]), abs(BASE_Y - point[1])


# Game features
CONST = {
    "MAX_X": 17_630,
    "MAX_Y": 9_000,

    "SPELL_WIND_RANGE": 1_280,

    "MONSTER_SPEED": 400,
    "MONSTER_TARGET_RANGE": 7_000,
    "MONSTER_DMG_RANGE": 300,

    "HERO_DMG": 2,
    "HERO_DMG_RANGE": 800,

}

HEROES = {}

WEIGHT_MODS = {
    "OFFENSIVE_POSITION": (MAX_X // 2, MAX_Y // 2),
    "ATTACK_POSITION": transpose((14_000, 6000)),
    "PRIMARY_DEFENDER_POSITION": transpose((MAX_X // 2, MAX_Y // 5)),
    "SECONDARY_DEFENDER_POSITION": transpose((MAX_X // 4, 2 * MAX_Y // 3)),

    "BASE_THREATENING_DISTANCE": 6000,
    "BASE_DANGER_DISTANCE": 4000,

    "PRIMARY_DEFENDERS": (1, 4),
    "SECONDARY_DEFENDERS": (2, 5),
    "ATTACKERS": (0, 3),

    "MOVE_THREAT": 50,

    "DEFENDER_POSITION_WEIGHT": 300,
    "ATTACKER_POSITION_WEIGHT": 400,

    "DISTANCE_TO_MONSTER_WEIGHT_DIV": 10,
}

WORLD = {
    "TURN": 0,

    "BASE": (BASE_X, BASE_Y),
    "ENEMY_BASE": transpose((CONST["MAX_X"], CONST["MAX_Y"])),

    "NUM_OF_MON_ATTACKING_US": 0,
    "NUM_OF_MON_IN_DANGER_ZONE": 0,
    "NUM_OF_MON_ATTACKING_ENEMY": 0,
}


def create_move(target_point, comment=""):
    return f"MOVE {target_point[0]} {target_point[1]} {comment}"


def create_wind(target_point, comment=""):
    return f"SPELL WIND {target_point[0]} {target_point[1]} {comment}"


def create_shield(entity_id, comment=""):
    return f"SPELL SHIELD {entity_id} {comment}"


def create_control(entity_id, target_point, comment=""):
    return f"SPELL CONTROL {entity_id} {target_point[0]} {target_point[1]} {comment}"


def create_wait():
    return "WAIT is it working?"


def main():
    while True:
        WORLD["TURN"] += 1
        for i in range(1):
            health, mana = [int(j) for j in input().split()]
            enemy_health, enemy_mana = [int(j) for j in input().split()]

        monsters, enemies = load_current_state()
        debug(f"STATE: {WORLD}")

        actions_per_hero = {}

        for hero_id, hero in HEROES.items():
            actions_per_hero[hero["id"]] = [hero["action"]]

        for hero_id, hero in HEROES.items():
            assign_movement_actions(actions_per_hero, hero, monsters)

            if mana > 10:
                assign_control_spell_actions(actions_per_hero, mana, hero, monsters)
                assign_shield_spells_actions(actions_per_hero, mana, hero, monsters)
                assign_wind_spells_actions(actions_per_hero, mana, hero, monsters)

        # Action/monster weight might be so big that it would warrant more than a single hero action
        # Score weight by action or by monster?

        debug(f"Actions: {actions_per_hero}")

        for hero_id, hero_action_list in actions_per_hero.items():
            hero_action_list.sort(key=lambda item: item[0], reverse=True)

            # if hero_id in WEIGHT_MODS["ATTACKERS"]:
            debug(f"Hero {hero_id} best ({hero_action_list[0][0]}) move: {hero_action_list[0][1]}")

            print(hero_action_list[0][1])


def assign_shield_spells_actions(actions_per_hero, current_mana, hero, monsters):
    best_spell = (-90000, create_wait(), None)
    if hero["type"] == HERO_TYPE_DEFENDER:
        return

    elif hero["type"] == HERO_TYPE_ATTACKER and current_mana > 30:
        for monster in monsters:
            # debug(f"Looking at: {monster['id']} shield: {monster['shield_life']}")
            distance_to_base = dist(WORLD["ENEMY_BASE"], monster["position"])
            # TODO: Marcin: refactor these invertions
            score = distance_to_base // ((distance_to_base / 2600) ** 2)
            # TODO: Marcin: Change it to evaluation i.e. num of enemy heroes, monster health, speed and distance to base

            if is_heading_towards_enemy_base(monster) and score < abs(best_spell[0]) \
                    and distance_to_base < 5000 \
                    and monster["shield_life"] < 2 \
                    and monster["health"] > 12:
                best_spell = (score, create_shield(monster["id"]), monster)

    if best_spell[2] is not None:
        best_spell[2]["is_targeted_by_spell"] = True
    actions_per_hero[hero["id"]].append((best_spell[0], best_spell[1], best_spell[2]))


def assign_wind_spells_actions(actions_per_hero, mana, hero, monsters):
    best_spell = (-90000, create_wait(), None)
    if hero["type"] == HERO_TYPE_DEFENDER:
        for monster in monsters:
            dist_to_base = dist(monster["position"], WORLD["BASE"])
            hero_monster_dist = dist(hero["position"], monster["position"])
            # TODO: Marcin: This can be simulated instead of hard-coded
            if dist_to_base < 3000 and hero_monster_dist <= 1280 and monster["shield_life"] == 0:
                best_spell = (99000, create_wind(WORLD["ENEMY_BASE"]), None)

    elif hero["type"] == HERO_TYPE_ATTACKER and mana > 30:
        for monster in monsters:
            monster_distance_to_en_base = dist(WORLD["ENEMY_BASE"], monster["position"])
            hero_distance_to_en_base = dist(WORLD["ENEMY_BASE"], hero["position"])
            hero_distance_to_monster = dist(monster["position"], hero["position"])

            debug(
                f"Attacker Wind score to mon {monster['id']}, for {monster_distance_to_en_base}, {hero_distance_to_en_base}, {hero_distance_to_monster}")

            if is_heading_towards_enemy_base(monster) \
                    and monster["shield_life"] == 0 \
                    and hero_distance_to_monster < CONST["SPELL_WIND_RANGE"] \
                    and monster_distance_to_en_base < 2500 \
                    and monster["health"] > 5:
                best_spell = (9999999, create_wind(WORLD["ENEMY_BASE"]), monster)

            if is_heading_towards_enemy_base(monster) \
                    and monster_distance_to_en_base < abs(best_spell[0]) \
                    and monster_distance_to_en_base < 6000 \
                    and monster["shield_life"] == 0 \
                    and hero_distance_to_monster < CONST["SPELL_WIND_RANGE"] \
                    and monster["health"] > 14:
                best_spell = (
                    monster_distance_to_en_base + 10 * monster["health"], create_wind(WORLD["ENEMY_BASE"]), monster)

    # TODO: Marcin: refactor
    if best_spell[2] is not None:
        best_spell[2]["is_targeted_by_spell"] = True

    if hero["id"] in WEIGHT_MODS["PRIMARY_DEFENDERS"]:
        actions_per_hero[hero["id"]].append((1000 * best_spell[0], best_spell[1], best_spell[2]))
    else:
        actions_per_hero[hero["id"]].append((best_spell[0], best_spell[1], best_spell[2]))


def assign_control_spell_actions(actions_per_hero, current_mana, hero, monsters):
    best_spell = (-90000, create_wait(), None)
    # if hero["type"] == HERO_TYPE_DEFENDER and (WORLD["NUM_OF_MON_ATTACKING_US"] > 2 or current_mana > 50):
    if hero["type"] == HERO_TYPE_DEFENDER and current_mana > 80:
        # Control spell
        for monster in monsters:
            hero_to_monster_dist = dist(monster["position"], hero["position"])
            # debug(
            #     f"Hero: {hero['id']} Mon: {monster['id']} dist: {hero_to_monster_dist} health: {monster['health']}, mana: {current_mana}, is_targ: {bool(monster['is_targeted_by_spell'])}, is_controlled: {monster['is_controlled']}")
            if hero_to_monster_dist < 2200 and monster["health"] > 14 and current_mana > 30 \
                    and not is_heading_towards_enemy_base(monster) \
                    and monster["near_base"] == 0 \
                    and not monster["is_targeted_by_spell"] and not monster["is_controlled"]:
                score = hero_to_monster_dist + monster["health"]

                # TODO: Marcin: Doing it for Nth time, time to refactor
                if best_spell[0] < score:
                    best_spell = (score, create_control(monster["id"], WORLD["ENEMY_BASE"]), monster)

    elif hero["type"] == HERO_TYPE_ATTACKER:
        return

    if best_spell[2] is not None:
        best_spell[2]["is_targeted_by_spell"] = True

    # Want one defender to prioritize CONTROL
    if hero["id"] in WEIGHT_MODS["PRIMARY_DEFENDERS"]:
        actions_per_hero[hero["id"]].append((1000 * best_spell[0], best_spell[1], best_spell[2]))
    else:
        actions_per_hero[hero["id"]].append((best_spell[0], best_spell[1], best_spell[2]))


def assign_movement_actions(actions_per_hero, hero, monsters):
    best_choice = (-9999999, None)

    if hero["type"] == HERO_TYPE_DEFENDER:

        for monster in monsters:
            monster_base_dist = dist(monster["position"], WORLD["BASE"])
            monster_hero_dist = dist(hero["position"], monster["position"])

            base_dist_score = monster_base_dist // ((monster_base_dist / 2000) ** 2)
            hero_dist_score = monster_hero_dist / WEIGHT_MODS["DISTANCE_TO_MONSTER_WEIGHT_DIV"]

            threat_score = 0
            if is_heading_towards_our_base(monster):
                threat_score = WEIGHT_MODS["MOVE_THREAT"]
                if monster_base_dist < WEIGHT_MODS["BASE_THREATENING_DISTANCE"]:
                    threat_score = threat_score + 500

            score = base_dist_score + threat_score - hero_dist_score

            # debug(
            #     f"Evaluating (hero: {hero['id']}) for monst: {monster['id']} as {score}: base_dist: {base_dist_score} and threat: {threat_score} and hero_dist {hero_dist_score} for distances: monst-base: {monster_base_dist} and hero-monst {monster_hero_dist}")

            if score >= best_choice[0]:
                best_choice = (score, monster)

        # TODO: Marcin: This is quite arbitrary...
        # Should probably be a formula of position and health
        # If not close enough, and not healthy enough...
        if best_choice[1] and not (
                dist(WORLD["BASE"], best_choice[1]["position"]) < CONST["MONSTER_TARGET_RANGE"] and best_choice[1][
            "health"] > 8):
            monsters.remove(best_choice[1])

        if best_choice[1]:
            x, y = best_choice[1]["position"]
            score = best_choice[0]
            actions_per_hero[hero["id"]].append((score, f"MOVE {x} {y}", best_choice[1]))

    elif hero["type"] == HERO_TYPE_ATTACKER:
        for monster in monsters:
            monster_hero_dist = dist(hero["position"], monster["position"])
            monster_base_dist = dist(WORLD["ENEMY_BASE"], monster["position"])
            monster_default_pos_dist = dist(hero["position"], hero["default_position"])

            # Don't chase too far
            if monster_default_pos_dist > 5000: continue
            # Don't go after monsters too close to enemy base...
            if monster_base_dist < 1500: continue

            monster_hero_score = monster_base_dist // ((monster_base_dist / 2000) ** 2)
            monster_default_pos_score = monster_default_pos_dist // 15
            score = monster_hero_score - monster_default_pos_score

            if is_heading_towards_enemy_base(monster):
                score = score - 50

            debug(
                f"Evalutating attacker for score {score} vs mon: {monster['id']}: {monster_hero_dist} {monster_base_dist} {monster_default_pos_dist} of scores: {monster_hero_score}, {monster_default_pos_score} for monst: {monster}")

            if score >= best_choice[0]:
                best_choice = (score, monster)

            # if monster_hero_dist < 2200 and 7_000 > monster_base_dist > best_choice[0]:
            #     best_choice = (monster_base_dist, monster)

    else:
        raise RuntimeError(f"Unknown hero type: {hero['type']}")

    if hero["type"] == HERO_TYPE_ATTACKER:
        debug(f"Attacking best move: {best_choice}")

    if best_choice[1]:
        x, y = best_choice[1]["position"]
        score = best_choice[0]
        actions_per_hero[hero["id"]].append((score, f"MOVE {x} {y}", best_choice[1]))


def load_current_state():
    my_heroes = []
    monsters = []
    enemies = []

    # Clear mutable data that is supposed to be reconstructed on each turn
    WORLD["NUM_OF_MON_ATTACKING_US"] = 0
    WORLD["NUM_OF_MON_ATTACKING_ENEMY"] = 0
    WORLD["NUM_OF_MON_IN_DANGER_ZONE"] = 0

    entity_count = int(input())  # Amount of heroes and monsters you can see
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero, 2=opponent hero
        # x: Position of this entity
        # shield_life: Ignore for this league; Count down until shield spell fades
        # is_controlled: Ignore for this league; Equals 1 when this entity is under a control spell
        # health: Remaining health of this monster
        # vx: Trajectory of this monster
        # near_base: 0=monster with no target yet, 1=monster targeting a base
        # threat_for: Given this monster's trajectory, is it a threat to 1=your base, 2=your opponent's base, 0=neither
        _id, _type, x, y, shield_life, is_controlled, health, vx, vy, near_base, threat_for = [int(j) for j in
                                                                                               input().split()]
        entity = {
            "id": _id,
            "_type": _type,
            "position": (x, y),
            "shield_life": shield_life,
            "is_controlled": bool(is_controlled),
            "health": health,
            "movement_vector": (vx, vy),
            "near_base": near_base,
            "threat_for": threat_for,
            "is_targeted_by_spell": False,
            "heroes_targeting_entity": []
        }

        if _type == 0:
            monsters.append(entity)
            if entity["threat_for"] == 1 and dist(WORLD["BASE"], entity["position"]) < WEIGHT_MODS[
                "BASE_THREATENING_DISTANCE"]:
                WORLD["NUM_OF_MON_ATTACKING_US"] += 1
            elif entity["threat_for"] == 2:
                WORLD["NUM_OF_MON_ATTACKING_ENEMY"] += 1
            if dist(WORLD["BASE"], entity["position"]) < WEIGHT_MODS["BASE_DANGER_DISTANCE"]:
                WORLD["NUM_OF_MON_IN_DANGER_ZONE"] += 1

        if _type == 1:
            my_heroes.append(entity)
        if _type == 2:
            enemies.append(entity)

    # TODO: Marcin: REFACTOR!
    for hero in my_heroes:
        hero_id = hero["id"]
        if hero_id in HEROES:
            HEROES[hero_id] = {**HEROES[hero["id"]], **hero}
        else:
            if hero_id in (0, 3):
                HEROES[hero_id] = {
                    "type": HERO_TYPE_ATTACKER,
                    "default_position": WEIGHT_MODS["OFFENSIVE_POSITION"],
                    "action": (WEIGHT_MODS["ATTACKER_POSITION_WEIGHT"], create_move(WEIGHT_MODS["OFFENSIVE_POSITION"])),
                    **hero
                }
            elif hero_id in (1, 4):
                HEROES[hero_id] = {
                    "type": HERO_TYPE_DEFENDER,
                    "default_position": WEIGHT_MODS["PRIMARY_DEFENDER_POSITION"],
                    "action": (
                        WEIGHT_MODS["DEFENDER_POSITION_WEIGHT"], create_move(WEIGHT_MODS["PRIMARY_DEFENDER_POSITION"])),
                    **hero
                }
            elif hero_id in (2, 5):
                HEROES[hero_id] = {
                    "type": HERO_TYPE_DEFENDER,
                    "default_position": WEIGHT_MODS["SECONDARY_DEFENDER_POSITION"],
                    "action": (
                        WEIGHT_MODS["DEFENDER_POSITION_WEIGHT"],
                        create_move(WEIGHT_MODS["SECONDARY_DEFENDER_POSITION"])),
                    **hero
                }

    if WORLD["TURN"] > 80:
        move_attacker_to_attack()

    return monsters, enemies


def move_attacker_to_attack():
    if 0 in HEROES:
        HEROES[0]["action"] = (
            WEIGHT_MODS["ATTACKER_POSITION_WEIGHT"],
            create_move(WEIGHT_MODS["ATTACK_POSITION"]))
        HEROES[0]["default_position"] = WEIGHT_MODS["ATTACK_POSITION"]
    else:
        HEROES[3]["action"] = (
            WEIGHT_MODS["ATTACKER_POSITION_WEIGHT"],
            create_move(WEIGHT_MODS["ATTACK_POSITION"]))
        HEROES[3]["default_position"] = WEIGHT_MODS["ATTACK_POSITION"]


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def is_heading_towards_enemy_base(monster):
    return monster["threat_for"] == 2


def is_heading_towards_our_base(monster):
    return monster["threat_for"] == 1


def debug(msg):
    print(msg, file=sys.stderr, flush=True)


def is_within_our_base(position):
    max_x, max_y = transpose((WEIGHT_MODS["BASE_THREATENING_DISTANCE"], WEIGHT_MODS["BASE_THREATENING_DISTANCE"]))
    if BASE_X == 0:
        return position[0] < max_x and position[1] < max_y
    else:
        return position[0] > max_x and position[1] > max_y


main()
