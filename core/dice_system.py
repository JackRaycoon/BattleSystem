import random

class DiceSystem:
    def __init__(self):
        self.battle_ui = None

    def d6(self, in_log = True):
        roll = random.randint(1, 6)
        if (in_log):
            self.battle_ui.add_log_message(f"[D6]: {roll}")
        return roll
    def d4(self, in_log = True):
        roll = random.randint(1, 4)
        if(in_log):
            self.battle_ui.add_log_message(f"[D4]: {roll}")
        return roll
    def d4x2(self):
        roll1 = self.d4(False)
        roll2 = self.d4(False)
        self.battle_ui.add_log_message(f"[2D4]: {roll1} + {roll2} = {roll1 + roll2}")
        return roll1 + roll2
    def d6x2(self):
        roll1 = self.d6(False)
        roll2 = self.d6(False)
        self.battle_ui.add_log_message(f"[2D6]: {roll1} + {roll2} = {roll1 + roll2}")
        return roll1 + roll2