"""Contains functions for running a basic challenge."""
from classes.features import Features
from classes.stats import Tracker
import ngucon as ncon
import usersettings as userset
import time


class Basic(Features):
    """Contains functions for running a basic challenge."""

    def first_rebirth(self):
        """Procedure for first rebirth after number reset."""
        end = time.time() + 3 * 60
        tm_unlocked = False
        bm_unlocked = False
        ci_assigned = False
        diggers = [2, 3, 8]
        self.loadout(1)
        self.nuke()
        time.sleep(2)
        self.fight()
        self.adventure(highest=True)
        while not tm_unlocked:
            if not ci_assigned:
                time.sleep(1)
                self.augments({"CI": 1}, 1e6)
                ci_assigned = True
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()

            tm_color = self.get_pixel_color(ncon.TMLOCKEDX, ncon.TMLOCKEDY)
            if tm_color != ncon.TMLOCKEDCOLOR:
                self.send_string("r")
                self.send_string("t")
                self.time_machine(True)
                self.loadout(2)
                tm_unlocked = True

        time.sleep(15)
        self.augments({"CI": 1}, 1e8)
        self.gold_diggers(diggers, True)
        self.adventure(highest=True)
        time.sleep(4)
        self.adventure(itopod=True, itopodauto=True)
        while not bm_unlocked:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

            bm_color = self.get_pixel_color(ncon.BMLOCKEDX, ncon.BMLOCKEDY)
            if bm_color != ncon.BMLOCKEDCOLOR:
                self.menu("bloodmagic")
                time.sleep(0.2)
                self.send_string("t")
                self.send_string("r")
                self.blood_magic(5)
                bm_unlocked = True
                self.augments({"SS": 0.7, "DS": 0.3}, 5e8)

        while time.time() < end:
            self.wandoos(True)
            self.nuke()
            time.sleep(2)
            self.fight()
            self.gold_diggers(diggers)
            time.sleep(5)

    def speedrun(self, duration, target):
        self.do_rebirth()
        start = time.time()
        end = time.time() + (duration * 60) + 1
        blood_digger_active = False
        itopod_advance = False
        self.nuke(125)
        self.loadout(1)  # Gold drop equipment
        self.adventure(highest=True)
        time.sleep(4)
        self.loadout(2)  # Bar/power equimpent
        self.adventure(itopod=True, itopodauto=True)
        self.time_machine(e=5e8, magic=True)
        self.augments({"AE": 0.75, "ES": 0.25}, 8e10)
        self.blood_magic(8)
        self.gold_diggers([4, 5, 6, 8, 9, 11, 12], True)
        self.wandoos(True)
        self.bb_ngu(3e9, [1, 2, 3, 4, 5, 6])
        self.bb_ngu(5e10, [7])  # drop
        self.bb_ngu(1.5e11, [8, 9], overcap=1.05)  # Magic NGU
        self.bb_ngu(4e9, [1], magic=True)
        self.bb_ngu(1e10, [2, 3, 4], magic=True, overcap=1.05)
        self.bb_ngu(1e11, [5], magic=True)  # TM
        self.bb_ngu(2e11, [6, 7], magic=True, overcap=1.05)  # Energy NGU
        while time.time() < end - 20:
            self.wandoos(True)
            self.gold_diggers([4, 5, 6, 8, 9, 11, 12])
            self.nuke()
        self.gold_diggers([9, 3, 5, 6], True)
        self.nuke()
        time.sleep(2)
        self.fight()
        self.pit(3)
        self.spin()
        self.save_check()
        while time.time() < end:
            time.sleep(0.1)
        while time.time() < end:
            try:
                """If current rebirth is scheduled for more than 3 minutes and
                we already finished the rebirth, we will return here, instead
                of waiting for the duration. Since we cannot start a new
                challenge if less than 3 minutes have passed, we must always
                wait at least 3 minutes."""

                current_boss = int(self.get_current_boss())
                if duration > 3 and current_boss > target:
                    if not self.check_challenge():
                        while time.time() < start + 180:
                            time.sleep(1)
                        return
                if current_boss < 101:
                    self.fight()

            except ValueError:
                print("OCR couldn't find current boss")
        return

    def check_challenge(self):
        """Check if a challenge is active."""
        self.rebirth()
        self.click(ncon.CHALLENGEBUTTONX, ncon.CHALLENGEBUTTONY)
        time.sleep(userset.LONG_SLEEP)
        color = self.get_pixel_color(ncon.CHALLENGEACTIVEX,
                                     ncon.CHALLENGEACTIVEY)

        return True if color == ncon.CHALLENGEACTIVECOLOR else False

    def basic(self, target):
        """Defeat target boss."""
        self.first_rebirth()

        for x in range(8):
            self.speedrun(3, target)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(7, target)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(12, target)
            if not self.check_challenge():
                return
        for x in range(5):
            self.speedrun(60, target)
            if not self.check_challenge():
                return
        return
