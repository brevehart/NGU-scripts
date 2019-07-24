"""24-hour rebirth script"""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.challenge import Challenge
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import UpgradeEM
from classes.window import Window

import coordinates as coords
import time


def speedrun(duration, f, rebirth=True, kill_titans=True, f_zone=6):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    rebirth -- True to start run with a rebirth
    kill_titans -- True to kill titans if run lasts long enough (only GRB for now)
    farm_zone -- zone number to farm, 0 for ITOPOD
    """

    elapsed_time = 0
    if rebirth:
        print("Rebirthing before speedrun")
        f.do_rebirth()
        print(f"Starting {duration}-minute speedrun")
    else:
        # subtract elapsed time from start
        elapsed_time = f.rebirth_time_to_sec(f.get_rebirth_time())
        print(f"Continuing {duration}-minute speedrun from {elapsed_time} seconds ({int(100 * elapsed_time / (duration * 60))}%).")

    start = time.time() - elapsed_time
    end = start + (duration * 60) + 1
    blood_digger_active = False
    itopod_advance = False
    is_farming = False
    f.nuke()
    time.sleep(2)
    f.nuke(48)
    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(8)
    # f.snipe(0, 1, highest=True, manual=True, bosses=True, once=True)
    # time.sleep(1)
    f.loadout(2)  # Bar/power equimpent
    f.basic_training(100)  # Currently, need to manually adjust amount (x2) to cap basics
    # f.adventure(itopod=True, itopodauto=True)
    # f.time_machine(1e8, magic=True)
    f.time_machine(1e5, 1)
    f.augments({"MI": 0.7, "DTMT": 0.3}, 1e5)

    f.blood_magic(1)
    f.merge_boost(12, 8)
    # f.boost_equipment()
    # f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # f.augments({"MI": 0.7, "DTMT": 0.3}, 1e5)
    # f.wandoos(True)
    lastMerge = start
    mergeInterval = 120
    while time.time() < end - 20:
        # f.wandoos(True)
        # f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
        if time.time() > start + 40:
            try:
                NGU_energy = f.get_idle_cap()
                # feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6, 7, 8, 9])
                NGU_magic = f.get_idle_cap(magic=True)
                # feature.assign_ngu(NGU_magic, [1, 2, 3, 4], magic=True)
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)
        if time.time() > start + 60 * 60 and kill_titans and "GRB" in f.titans_available():
            f.kill_titan("GRB")
            is_farming = False
        elif time.time() > start + 90 and f_zone > 0 and not is_farming:
            f.adventure(zone=f_zone)
            is_farming = True
            print(f"Farming zone target: {f_zone}, actual: {f.get_adv_zone()}, current boss: {f.get_current_boss()}.")
        elif time.time() > start + 90 and not itopod_advance and not is_farming:
            f.adventure(itopod=True, itopodauto=True)
            itopod_advance = True
            print(f"Why are we doing ITOPOD? fz: {f_zone} {f.get_adv_zone()}, is_farming: {is_farming}")
        if time.time() > lastMerge + mergeInterval:
            elapsed = time.time() - start
            percent_elapsed = int(100 * elapsed / (end - start))
            print(f"Maintenance: {int(elapsed)} seconds from rebirth start ({percent_elapsed}%).")
            f.blood_magic(1)
            f.nuke()
            f.time_machine(1e5, 1)  # add checks to get current allocation or just remove before adding
            f.augments({"MI": 0.7, "DTMT": 0.3}, 1e5)
            f.cap_last_basic_training()  # possibly only run once at 25 min( or less with perks/quirks)
            f.merge_boost(12, 8)
            lastMerge = time.time()

    # end of rebirth actions
    f.nuke()
    time.sleep(2)
    f.fight()
    f.pit()
    f.spin()
    f.save_check()
    f.ygg()
    tracker.progress()
    u.buy()
    tracker.adjustxp()
    while time.time() < end:
        time.sleep(0.1)

    return


def farm_zone(zoneZ, duration, f, idle=False):
    """Start a farming run.

    Keyword arguments
    zoneZ -- zone number to farm
    duration -- duration in seconds to run
    f -- feature object
    idle -- if true, uses idle attack
    """
    print("{0:^40}".format(tracker.elapsed_time()))

    f.merge_boost(12, 8)
    if idle:
        f.adventure(zone=zoneZ)
        time.sleep(duration)
    else:
        f.snipe(zoneZ, duration // 60)  # convert to minutes

    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = UpgradeEM(37500, 37500, 2, 2, 3, report=True)

print(w.x, w.y)

tracker = Tracker(5)
c = Challenge()

feature.kill_titan("GRB")
# for spell_num in feature.check_spells_ready():
#     feature.cast_spell(spell_num)
# feature.toggle_auto_spells(number=True, drop=False, gold=False)
quit()
speedrun(30, feature, rebirth=False)

while True:  # main loop
    # feature.questing()
    # feature.itopod_snipe(300) # duration in seconds
    tracker.progress()
    # feature.merge_boost(12, 8) # m/b equip then merge one row (12) and boost 8 slots

    # farm_zone(5, 60, feature)
    # feature.boost_cube()
    # feature.ygg()
    # feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    # time.sleep(120)
    # c.start_challenge(9)
    speedrun(30, feature)  # duration in minutes
