from core.character import Character
from core.dice_system import DiceSystem


class BattleCore:
    def __init__(self, dice_system):
        self.player = None
        self.enemy = None
        self.battle_ui = None
        self.dice_system = dice_system
        self.init_characters()

    def init_characters(self):
        from core.character import Player, Enemy
        self.player = Player()
        self.enemy = Enemy()

    def hit(self):
        roll = self.dice_system.d6()
        match roll:
            case x if x <= 2:
               self.battle_ui.add_log_message("Промах!")
            case x if x >=3:
                self.battle_ui.add_log_message("Попадание!")
                self.enemy.take_damage(1)
        self.battle_ui.update_health_bars()
