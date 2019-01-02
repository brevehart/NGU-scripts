"""3-minute rebirth script"""

# Challenges
from challenges.basic import Basic
from challenges.level import Level

# Helper classes
from classes.discord import Discord
from classes.features import Features
from classes.inputs import Inputs
from classes.navigation import Navigation
from classes.stats import Stats, EstimateRate, Tracker
from classes.upgrade import Upgrade
from classes.window import Window

import ngucon as ncon
import time


def speedrun(duration, f):
    """Start a speedrun.

    Keyword arguments
    duration -- duration in minutes to run
    f -- feature object
    """
    f.do_rebirth()
    start = time.time()
    end = time.time() + (duration * 60) + 1
    blood_digger_active = False
    itopod_advance = False
    f.nuke(125)
    f.loadout(1)  # Gold drop equipment
    f.adventure(highest=True)
    time.sleep(4)
    f.loadout(2)  # Bar/power equimpent
    f.adventure(itopod=True, itopodauto=True)
    f.time_machine(e=5e8, magic=True)
    f.augments({"AE": 0.75, "ES": 0.25}, 8e10)
    f.blood_magic(8)
    f.gold_diggers([4, 5, 6, 8, 9, 11, 12], True)
    f.wandoos(True)
    f.bb_ngu(3e9, [1, 2, 3, 4, 5, 6])
    f.bb_ngu(5e10, [7])  # drop
    f.bb_ngu(1.5e11, [8])  # Magic NGU
    f.bb_ngu(4e9, [1], magic=True)
    f.bb_ngu(1e10, [2, 3, 4], magic=True)
    f.bb_ngu(1e11, [5], magic=True)  # TM
    f.bb_ngu(1e11, [6], magic=True)  # Energy NGU
    while time.time() < end - 20:
        f.wandoos(True)
        f.gold_diggers([4, 5, 6, 8, 9, 11, 12])
        if time.time() > start + 40:
            try:
                #NGU_energy = int(f.remove_letters(f.ocr(ncon.OCR_ENERGY_X1, ncon.OCR_ENERGY_Y1, ncon.OCR_ENERGY_X2, ncon.OCR_ENERGY_Y2)))
                #feature.assign_ngu(NGU_energy, [1, 2, 4, 5, 6, 7, 8])
                #NGU_magic = int(f.remove_letters(f.ocr(ncon.OCR_MAGIC_X1, ncon.OCR_MAGIC_Y1, ncon.OCR_MAGIC_X2, ncon.OCR_MAGIC_Y2)))
                #feature.assign_ngu(NGU_magic, [2, 3, 4], magic=True)
                if not f.check_bb_ngu(8):
                    f.bb_ngu(1e11, [9], recheck=True)
                else:
                    f.assign_ngu(1e12, [8])
                if not f.check_bb_ngu(5, magic=True):
                    f.bb_ngu(1e11, [5], magic=True, recheck=True)
                else:
                    f.assign_ngu(1e12, [6], magic=True)
            except ValueError:
                print("couldn't assign e/m to NGUs")
            time.sleep(0.5)
        if time.time() > start + 90 and not itopod_advance:
            f.adventure(itopod=True, itopodauto=True)
            itopod_advance = True

    f.gold_diggers([9, 3, 5, 6], True)
    f.nuke()
    time.sleep(2)
    f.fight()
    f.pit(3)
    f.spin()
    f.save_check()
    tracker.progress()
    u.em()
    tracker.adjustxp()
    #f.speedrun_bloodpill()
    while time.time() < end:
        time.sleep(0.1)

    return


w = Window()
i = Inputs()
nav = Navigation()
feature = Features()

Window.x, Window.y = i.pixel_search(ncon.TOP_LEFT_COLOR, 100, 100, 400, 600)
nav.menu("inventory")

u = Upgrade(37500, 37500, 4, 4, 1)

print(w.x, w.y)
tracker = Tracker(3)
#c = Challenge(tracker)
#print(c.check_challenge())

#u.em()
#feature.bb_ngu(4e8, [1, 2, 3, 4, 5, 6, 7, 8, 9], 1.05)
#feature.speedrun_bloodpill()
NGU_energy = int(feature.remove_letters(feature.ocr(ncon.OCR_ENERGY_X1, ncon.OCR_ENERGY_Y1, ncon.OCR_ENERGY_X2, ncon.OCR_ENERGY_Y2)))
NGU_magic = int(feature.remove_letters(feature.ocr(ncon.OCR_MAGIC_X1, ncon.OCR_MAGIC_Y1, ncon.OCR_MAGIC_X2, ncon.OCR_MAGIC_Y2)))
print(NGU_magic, NGU_energy)
#feature.assign_ngu(NGU_magic, [2, 3, 4], magic=True)
#while True:  # main loop
    #feature.boost_equipment()
    #feature.merge_inventory(12)
    #feature.boost_inventory(7)
    
    #feature.ygg()
    #feature.itopod_snipe(180)
    #Discord.send_message("Still going strong", 0)
    #speedrun(3, feature)
