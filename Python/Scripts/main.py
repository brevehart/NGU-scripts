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
# from classes.utilities import Utilities

import coordinates as coords
import time


def speedrun(duration, f, rebirth=True, kill_titans=True, f_zone=80):
    """Start a speedrun. Doesn't have to be very speedy though.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    rebirth -- True to start run with a rebirth
    kill_titans -- True to kill titans if run lasts long enough
    farm_zone -- zone number to farm, 0 for ITOPOD
    """

    elapsed_time = 0
    if rebirth:
        print(f"Rebirthing before speedrun. Current boss: {f.get_current_boss()}")
        f.do_rebirth()
        print(f"Starting {duration}-minute speedrun")
    else:
        # subtract elapsed time from start
        elapsed_time = f.rebirth_time_to_sec(f.get_rebirth_time())
        print(f"Continuing {duration}-minute speedrun from {elapsed_time} seconds "
              f"({100 * elapsed_time / (duration * 60):.1f}%).")

    start = time.time() - elapsed_time
    end = start + (duration * 60) + 1
    blood_digger_active = False
    itopod_advance = False
    is_farming = False
    em_distribution_complete = False
    cap_factor = 0.999
    f.nuke()
    time.sleep(2)
    f.nuke(48)
    current_boss = f.get_current_boss()
    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(8)
    # f.snipe(0, 1, highest=True, manual=True, bosses=True, once=True)
    # time.sleep(1)
    f.loadout(2)  # Bar/power equimpent
    # f.basic_training(100)  # Currently, need to manually adjust amount (x2) to cap basics
    # f.adventure(itopod=True, itopodauto=True)
    # f.time_machine(1e8, magic=True)
    f.time_machine(1e5, 2e4)
    f.augments({"MI": 0.7, "DTMT": 0.3}, 1e5)

    f.blood_magic(1)
    # f.merge_boost(12, 8)
    # f.boost_equipment()
    # f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
    # f.augments({"MI": 0.7, "DTMT": 0.3}, 1e5)
    # f.wandoos(True)

    # settings for loop
    maintenance_interval = 120
    # settings for E/M distribution
    ratios = {"advanced_training": 1 / 3, "time_machine": (1 / 6, 1 / 4), "augments": 1 / 4,
              'blood_magic': 1, "wandoos": 1 / 5, "ngu": 0.01}
    augments = {"SS": 0.8, "DS": 0.2}
    limits = {"time_machine": (4e5, 4e4)}
    max_ritual = 1

    # loop constants and variables
    ONE_HOUR = 3600  # for titans and ygg, might need to separate these after ygg perks/quirks
    next_zone_unlock_boss = 0
    max_zone = 0
    last_maintenance = start
    last_hour = start
    last_attempted_spell_cast = 0

    # main loop
    while time.time() < end - 20:
        if time.time() > start + 40:
            try:
                NGU_energy = f.get_idle_cap()
                # feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6, 7, 8, 9])
                NGU_magic = f.get_idle_cap(magic=True)
                # feature.assign_ngu(NGU_magic, [1, 2, 3, 4], magic=True)
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)

        if time.time() >= max(start + ONE_HOUR, last_maintenance + maintenance_interval) and kill_titans:
            if f.fight_titans():  # fights any available titans, returns True if any were available
                is_farming = False

        if time.time() > start + 90 and f_zone > 0 and not is_farming:
            m_zone, max_zone, next_zone_unlock_boss = f.get_max_adv_zone(zone=f_zone)
            f.adventure(zone=m_zone, highest=False)
            is_farming = True
            print(f"Farming: target zone: {f_zone}, actual: {f.get_adv_zone()}, max zone: {max_zone}, "
                  f"current boss: {f.get_current_boss()}, boss needed for next zone: {next_zone_unlock_boss + 1}.")
            # f.menu("adventure")
        elif time.time() > start + 90 and not itopod_advance and not is_farming:
            f.adventure(itopod=True, itopodauto=True)
            itopod_advance = True
            print(f"Why are we doing ITOPOD? fz: {f_zone} {f.get_adv_zone()}, is_farming: {is_farming}")

        if time.time() > last_maintenance + maintenance_interval:  # common tasks
            elapsed = time.time() - start
            percent_elapsed = int(100 * elapsed / (end - start))
            print(f"Maintenance: {int(elapsed)} seconds from rebirth start ({percent_elapsed}%).")
            f.nuke()
            f.fight()
            the_boss = f.get_current_boss()
            if the_boss > next_zone_unlock_boss and f_zone > max_zone:
                is_farming = False  # reset flag so we try to reach our target zone if boss limited

            if not em_distribution_complete:
                em_distribution_complete = f.distribute_em(max_ritual=max_ritual, ratios=ratios, augments=augments,
                                                           limits=limits, cap_factor=cap_factor, report=True)
                time.sleep(0.5)

            if f.check_dead_in_adv():
                print("Died in adventure mode. Consider decreasing farm_zone.")
                is_farming = False

            # f.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])
            # f.cap_last_basic_training()  # possibly only run once at 25 min
            f.merge_boost(merge=18, boost=8, transform=2)
            spelled = False
            if time.time() > last_attempted_spell_cast + 5 * maintenance_interval:  # spells are not available very frequently
                for spell_num in feature.check_spells_ready():
                    feature.cast_spell(spell_num)  # add check for evil mode spell #3?
                    spelled = True
                    is_farming = False  # cast_spell changes farm zone to itopod

            last_maintenance = time.time()
            if spelled:
                feature.toggle_auto_spells(number=True, drop=False, gold=False)
                last_attempted_spell_cast = last_maintenance

        if time.time() >= last_hour + ONE_HOUR:  # hourly tasks
            elapsed = time.time() - start
            percent_elapsed = int(100 * elapsed / (end - start))
            print(f"Hourly tasks at {int(elapsed)} seconds ({percent_elapsed:.1f}%)")
            f.fight_titans()
            f.ygg()
            last_hour = time.time()

    print("Preparing for rebirth.")
    f.nuke()
    time.sleep(2)
    f.fight()
    f.pit()
    f.spin()
    f.save_check()
    f.ygg(eat_all=True)
    f.fight_titans()
    tracker.progress()
    u.buy()
    tracker.adjustxp()
    while time.time() < end:
        time.sleep(0.1)
    f.fight_titans(debug=True)  # just in case we missed them by a few seconds
    f.ygg(eat_all=True)

    return


def farm_adv(duration, f, zone=1000, idle=False):
    """Start a farming run.

    Keyword arguments
    duration -- duration in seconds to run
    f -- feature object
    zone -- zone number to farm, default 1000 (i.e., 'highest')
    idle -- if true, uses idle attack, else manually fights
    """
    print("{0:^40}".format(tracker.elapsed_time()))

    f.merge_boost(merge=12, boost=8, transform=2)
    f.auto_titans()
    if idle:
        f.adventure(zone=zone)
        time.sleep(int(duration))
    else:
        f.snipe(zone, int(duration) / 60)  # convert to minutes

    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(coords.TOP_LEFT_COLOR, 0, 0, 400, 600)
nav.menu("inventory")

u = UpgradeEM(37500, 37500, 1, 1, 8, report=True)

print(w.x, w.y)

tracker = Tracker(5)
c = Challenge()

feature.titans_available(debug=True)
print(f"max_adv_zone: {feature.get_max_adv_zone()}")
feature.get_rebirth_time(debug=True)

speedrun(61, feature, rebirth=False)

while True:  # main loop
    # feature.questing()
    # feature.itopod_snipe(300) # duration in seconds
    # tracker.progress()
    # feature.merge_boost(12, 8) # m/b equip then merge one row (12) and boost 8 slots

    # farm_adv(60, feature, zone=600)
    # feature.boost_cube()
    # feature.ygg()
    # feature.gold_diggers([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12])

    # time.sleep(120)
    # c.start_challenge(9)
    speedrun(61, feature)  # duration in minutes
