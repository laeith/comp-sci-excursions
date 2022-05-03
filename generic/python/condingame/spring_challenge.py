import math
import sys
from enum import Enum

# https://www.codingame.com/ide/challenge/spring-challenge-2022

# The code here is what I did after around ~10h+ of CodinGame Spring Challenge, at the very start it got me fairly high
# into TOP 70, unfortunately after ~7 days of inactivity the bot got demoted into TOP 800.
# Yes, it's ugly, and quite bad. Probably acceptable for a first try at this type of challenges.

# A list of things to do:
# No monster in enemy zone -> Attacker go middle
# A lot of monsters in enemy, some without shield -> Dive and wind
# Improve defenders, probably should take into account enemy attacker position, at least for one of defenders
# There is an issue where a hero having far higher distance to a monster is assigned to chase it to the base
#     If no enemy heroes -> simulate if 1 is enough
#     If enemy heroes -> send both if within our base range
# Looks like this is the biggest bottleneck at the moment
# Make the closer defender go to the monster attacking base
# Farming still not that great
# Wind -> Shield combo more efficient
# Control of enemy hero if score guaranteed
# Don't attack monsters in enemy base
# Dive if simulation succeeds
# Shield for enemies close to base that can be killed but threatened by enemies
# We can actually calculate if more than a single defender is needed (but need to take into account enemy)
# At least one defender should prio defense over control
# Well, now defenders are too aggresive with control
# Marcin: Add 'wandering mode' if nothing to do
# Marcin: Middle defender sticks too hard initially to middle position
# MORE 'states' e.g. if there are many monsters in enemy base then 'dive mode'
# Simulate if it's better to use wind or just hit to death (rist that enemy will wind it into my base)
# Handle fog of war
# Rework most of it to a more general, intelligent approach

MAX_X = 17_630
MAX_Y = 9_000

BASE_X, BASE_Y = [int(i) for i in input().split()]
HEROES_PER_PLAYER = int(input())


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
    "HERO_LINE_OF_SIGHT": 2200,
}

WEIGHT_MODS = {
    "BASE_THREATENING_DISTANCE": 7500,
    "BASE_DANGER_DISTANCE": 4000,

    "PRIMARY_DEFENDERS": (1, 4),
    "SECONDARY_DEFENDERS": (2, 5),
    "ATTACKERS": (0, 3),

    "MOVE_THREAT": 100,

    "DISTANCE_TO_MONSTER_WEIGHT_DIV": 10,

    "ENEMY_BASE_THREATENING_DISTANCE": 8000,
}

WORLD = {
    "TURN": 0,

    "BASE": (BASE_X, BASE_Y),
    "ENEMY_BASE": transpose((CONST["MAX_X"], CONST["MAX_Y"])),
    "BASE_RADIUS": 5000,

    "NUM_OF_MON_ATTACKING_US": 0,
    "NUM_OF_MON_IN_DANGER_ZONE": 0,
    "NUM_OF_MON_ATTACKING_ENEMY": 0,
    "NUM_OF_MON_THREATENING_ENEMY": 0,
    "NUM_OF_EN_HEROES_IN_THREATENING_ZONE": 0,
    "DEFENDERS_IN_ENEMY_BASE": 0,
    "SEEN_ENEMIES": 0,
}

HEROES = {}


class Hero():
    def __init__(self, id, stance, entity_properties):
        self.id = id
        self.stance = stance
        self.properties = entity_properties


class Stance(Enum):
    ATTACK = (transpose((14_000, 6000)), 300)
    PRIMARY_DEFENSE = (transpose((MAX_X // 2, MAX_Y // 7)), 250)
    SECONDARY_DEFENSE = (transpose((MAX_X // 5, 6 * MAX_Y // 7)), 250)
    ROAM_MIDDLE = (transpose((MAX_X // 2, 6 * MAX_Y // 7)), 200)
    DIVE = (transpose((1450, 1450)), 600)

    def __init__(self, position, position_weight):
        self.position = position
        self.position_weight = position_weight


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

        for hero in HEROES.values():
            actions_per_hero[hero.id] = [(hero.stance.position_weight, create_move(hero.stance.position))]

        for hero in HEROES.values():
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

            debug(f"Hero {hero_id} best ({hero_action_list[0][0]}) move: {hero_action_list[0][1]}")

            print(hero_action_list[0][1])


def assign_shield_spells_actions(actions_per_hero, current_mana, hero, monsters):
    best_spell = (-90000, create_wait(), None)
    if hero.stance in [Stance.PRIMARY_DEFENSE, Stance.SECONDARY_DEFENSE]:
        return

    elif hero.stance == Stance.ATTACK and current_mana > 30:
        for monster in monsters:
            # debug(f"Looking at: {monster['id']} shield: {monster['shield_life']}")
            distance_to_base = dist(WORLD["ENEMY_BASE"], monster["position"])
            # TODO: Marcin: refactor these invertions
            score = distance_to_base // ((distance_to_base / 2600) ** 2)
            # TODO: Marcin: Change it to evaluation i.e. num of enemy heroes, monster health, speed and distance to base

            if is_heading_towards_enemy_base(monster) and score < abs(best_spell[0]) \
                    and distance_to_base < 4000 \
                    and monster["shield_life"] < 2 \
                    and monster["health"] > 12:
                best_spell = (9000, create_shield(monster["id"]), monster)

    if best_spell[2] is not None:
        best_spell[2]["is_targeted_by_spell"] = True
    actions_per_hero[hero.id].append((best_spell[0], best_spell[1], best_spell[2]))


def assign_wind_spells_actions(actions_per_hero, mana, hero, monsters):
    best_spell = (-90000, create_wait(), None)
    if hero.stance in [Stance.PRIMARY_DEFENSE, Stance.SECONDARY_DEFENSE]:
        for monster in monsters:
            dist_to_base = dist(monster["position"], WORLD["BASE"])
            hero_monster_dist = dist(hero.properties["position"], monster["position"])
            # TODO: Marcin: This can be simulated instead of hard-coded
            if dist_to_base < 3000 and hero_monster_dist <= 1280 and monster["shield_life"] == 0:
                best_spell = (99000, create_wind(WORLD["ENEMY_BASE"]), None)

    elif hero.stance == Stance.ATTACK and mana > 30:
        if WORLD["DEFENDERS_IN_ENEMY_BASE"] == 3:
            return

        for monster in monsters:
            monster_distance_to_en_base = dist(WORLD["ENEMY_BASE"], monster["position"])
            hero_distance_to_en_base = dist(WORLD["ENEMY_BASE"], hero.properties["position"])
            hero_distance_to_monster = dist(monster["position"], hero.properties["position"])

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
                    and monster_distance_to_en_base < 7000 \
                    and monster["shield_life"] == 0 \
                    and hero_distance_to_monster < CONST["SPELL_WIND_RANGE"] \
                    and monster["health"] > 14:
                best_spell = (
                    monster_distance_to_en_base * 2 + 10 * monster["health"], create_wind(WORLD["ENEMY_BASE"]), monster)

    # TODO: Marcin: refactor
    if best_spell[2] is not None:
        best_spell[2]["is_targeted_by_spell"] = True

    if hero.id in WEIGHT_MODS["PRIMARY_DEFENDERS"]:
        actions_per_hero[hero.id].append((1000 * best_spell[0], best_spell[1], best_spell[2]))
    else:
        actions_per_hero[hero.id].append((best_spell[0], best_spell[1], best_spell[2]))


def assign_control_spell_actions(actions_per_hero, current_mana, hero, monsters):
    best_spell = (-90000, create_wait(), None)
    if hero.stance in [Stance.PRIMARY_DEFENSE, Stance.SECONDARY_DEFENSE] and current_mana > 80:
        for monster in monsters:
            hero_to_monster_dist = dist(monster["position"], hero.properties["position"])
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

    elif hero.stance == Stance.ATTACK:
        threatening_monsters = all_monsters_within_distance(monsters, WORLD["ENEMY_BASE"],
                                                            WEIGHT_MODS["BASE_THREATENING_DISTANCE"])
        if not threatening_monsters:
            for monster in monsters:
                hero_to_monster_dist = dist(monster["position"], hero.properties["position"])
                if hero_to_monster_dist < 2200 and monster["health"] > 14 and current_mana > 30 \
                        and not is_heading_towards_enemy_base(monster) \
                        and monster["near_base"] == 0 \
                        and not monster["is_targeted_by_spell"] and not monster["is_controlled"]:
                    score = hero_to_monster_dist + monster["health"]

                    # TODO: Marcin: Doing it for Nth time, time to refactor
                    if best_spell[0] < score:
                        best_spell = (score, create_control(monster["id"], WORLD["ENEMY_BASE"]), monster)
        else:
            return

    if best_spell[2] is not None:
        best_spell[2]["is_targeted_by_spell"] = True

    # Want one defender to prioritize CONTROL?
    if hero.id in WEIGHT_MODS["PRIMARY_DEFENDERS"]:
        actions_per_hero[hero.id].append((1000 * best_spell[0], best_spell[1], best_spell[2]))
    else:
        actions_per_hero[hero.id].append((best_spell[0], best_spell[1], best_spell[2]))


def assign_movement_actions(actions_per_hero, hero, monsters):
    best_choice = (-9999999, None)

    if hero.stance in [Stance.PRIMARY_DEFENSE, Stance.SECONDARY_DEFENSE]:
        for monster in monsters:
            monster_base_dist = dist(monster["position"], WORLD["BASE"])
            monster_hero_dist = dist(hero.properties["position"], monster["position"])

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
        # If not close enough, and not healthy enough, not threatened...
        if best_choice[1] and not (
                dist(WORLD["BASE"], best_choice[1]["position"]) < CONST["MONSTER_TARGET_RANGE"] and best_choice[1][
            "health"] > 8):
            monsters.remove(best_choice[1])

        if best_choice[1]:
            x, y = best_choice[1]["position"]
            score = best_choice[0]
            actions_per_hero[hero.id].append((score, f"MOVE {x} {y}", best_choice[1]))

    elif hero.stance == Stance.ROAM_MIDDLE:
        nearby_monsters = all_monsters_within_distance(monsters, hero.properties["position"],
                                                       CONST["HERO_LINE_OF_SIGHT"])
        if nearby_monsters:
            for monster in nearby_monsters:
                monster_hero_dist = dist(hero.properties["position"], monster["position"])
                monster_default_pos_dist = dist(monster["position"], hero.stance.position)

                if ((monster_hero_dist / 1400) ** 2) != 0:
                    monster_hero_score = monster_hero_dist // ((monster_hero_dist / 1400) ** 2)
                else:
                    monster_hero_score = 9999  # monster on hero
                monster_default_pos_score = (monster_default_pos_dist // 90) ** 2
                score = monster_hero_score - monster_default_pos_score

                threat_score = 0
                if is_heading_towards_our_base(monster):
                    threat_score = WEIGHT_MODS["MOVE_THREAT"]

                if is_heading_towards_enemy_base(monster):
                    score = score - 100

                score = score + threat_score

                debug(
                    f"Evalutating attacker for score {score} vs mon: {monster['id']}: {monster_hero_dist} {monster_default_pos_dist} of scores: {monster_hero_score}, {monster_default_pos_score} for monst: {monster}")

                if score >= best_choice[0]:
                    best_choice = (score, monster)
        else:
            x, y = hero.stance.position
            new_x, new_y = transpose((x, y - 2100))
            if dist(hero.properties["position"], hero.stance.position) < 2100:
                actions_per_hero[hero.id].append((400, f"MOVE {new_x} {new_y}", best_choice[1]))

    elif hero.stance == Stance.ATTACK:
        for monster in monsters:
            monster_hero_dist = dist(hero.properties["position"], monster["position"])
            monster_base_dist = dist(WORLD["ENEMY_BASE"], monster["position"])
            monster_default_pos_dist = dist(monster["position"], hero.stance.position)

            # Don't go after monsters too close to enemy base...
            if monster_base_dist < 1500: continue

            # Don't chase too far
            if monster_default_pos_dist > 7000 and WORLD["DEFENDERS_IN_ENEMY_BASE"] != 3:
                continue

            monster_hero_score = monster_base_dist // ((monster_base_dist / 2000) ** 2)
            monster_default_pos_score = monster_default_pos_dist // 15
            score = monster_hero_score - monster_default_pos_score

            if is_heading_towards_enemy_base(monster) and monster_base_dist < 4000:
                continue

            debug(
                f"Evalutating attacker for score {score} vs mon: {monster['id']}: {monster_hero_dist} {monster_base_dist} {monster_default_pos_dist} of scores: {monster_hero_score}, {monster_default_pos_score} for monst: {monster}")

            if score >= best_choice[0]:
                best_choice = (score, monster)

    else:
        raise RuntimeError(f"Unknown hero type: {hero.properties['type']}")

    if hero.stance == Stance.ATTACK:
        debug(f"Attacking best move: {best_choice}")

    if best_choice[1]:
        x, y = best_choice[1]["position"]
        score = best_choice[0]
        actions_per_hero[hero.id].append((score, f"MOVE {x} {y}", best_choice[1]))


def load_current_state():
    my_heroes = []
    monsters = []
    enemies = []

    # Clear mutable data that is supposed to be recalculated on each turn
    WORLD["NUM_OF_MON_ATTACKING_US"] = 0
    WORLD["NUM_OF_MON_ATTACKING_ENEMY"] = 0
    WORLD["NUM_OF_MON_THREATENING_ENEMY"] = 0
    WORLD["NUM_OF_MON_IN_DANGER_ZONE"] = 0
    WORLD["NUM_OF_EN_HEROES_IN_THREATENING_ZONE"] = 0
    WORLD["DEFENDERS_IN_ENEMY_BASE"] = 0
    WORLD["SEEN_ENEMIES"] = 0

    entity_count = int(input())  # Amount of heroes and monsters you can see
    for i in range(entity_count):
        # _id: Unique identifier
        # _type: 0=monster, 1=your hero_properties, 2=opponent hero_properties
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

        entity_en_base_dist = dist(WORLD["ENEMY_BASE"], entity["position"])
        entity_my_base_dist = dist(WORLD["BASE"], entity["position"])

        if _type == 0:
            monsters.append(entity)
            if entity["threat_for"] == 1 and entity_my_base_dist < WEIGHT_MODS["BASE_THREATENING_DISTANCE"]:
                WORLD["NUM_OF_MON_ATTACKING_US"] += 1
            elif entity["threat_for"] == 2 and entity_en_base_dist < WORLD["BASE_RADIUS"]:
                WORLD["NUM_OF_MON_ATTACKING_ENEMY"] += 1
            elif entity["threat_for"] == 2 \
                    and WORLD["BASE_RADIUS"] < entity_en_base_dist < WEIGHT_MODS["ENEMY_BASE_THREATENING_DISTANCE"]:
                WORLD["NUM_OF_MON_ATTACKING_ENEMY"] += 1

            if entity_my_base_dist < WEIGHT_MODS["BASE_DANGER_DISTANCE"]:
                WORLD["NUM_OF_MON_IN_DANGER_ZONE"] += 1

        if _type == 1:
            my_heroes.append(entity)
        if _type == 2:
            enemies.append(entity)
            WORLD["SEEN_ENEMIES"] += 1
            if entity_my_base_dist < WEIGHT_MODS["BASE_THREATENING_DISTANCE"]:
                WORLD["NUM_OF_EN_HEROES_IN_THREATENING_ZONE"] += 1
            if entity_en_base_dist < WEIGHT_MODS["BASE_THREATENING_DISTANCE"]:
                WORLD["DEFENDERS_IN_ENEMY_BASE"] += 1

    # TODO: Marcin: Ekhem...
    for hero_properties in my_heroes:
        hero_id = hero_properties["id"]
        if hero_id in HEROES:
            HEROES[hero_id].properties = hero_properties
        else:
            if hero_id in (0, 3):
                HEROES[hero_id] = Hero(hero_id, Stance.ROAM_MIDDLE, hero_properties)
            elif hero_id in (1, 4):
                HEROES[hero_id] = Hero(hero_id, Stance.PRIMARY_DEFENSE, hero_properties)
            elif hero_id in (2, 5):
                HEROES[hero_id] = Hero(hero_id, Stance.SECONDARY_DEFENSE, hero_properties)

    if WORLD["TURN"] > 80:
        for i in WEIGHT_MODS["ATTACKERS"]:
            if i in HEROES:
                HEROES[i].stance = Stance.ATTACK

    return monsters, enemies


def dist(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def is_heading_towards_enemy_base(monster):
    return monster["threat_for"] == 2


def is_heading_towards_our_base(monster):
    return monster["threat_for"] == 1


def all_monsters_within_distance(monsters, position, distance):
    return [monster for monster in monsters if dist(monster["position"], position) <= distance]


def debug(msg):
    print(msg, file=sys.stderr, flush=True)


def is_within_threatening_distance(position):
    max_x, max_y = transpose((WEIGHT_MODS["BASE_THREATENING_DISTANCE"], WEIGHT_MODS["BASE_THREATENING_DISTANCE"]))
    if BASE_X == 0:
        return position[0] < max_x and position[1] < max_y
    else:
        return position[0] > max_x and position[1] > max_y


main()
