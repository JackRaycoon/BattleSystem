from core.character import AttackType


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
                dmg = 0
                if self.crit_check(self.enemy):
                    self.battle_ui.add_log_message("Критический удар!")
                    dmg = self.damage_calc(self.player.attack_type, True)
                else:
                    dmg = self.damage_calc(self.player.attack_type)
                self.enemy.take_damage(dmg)
                self.battle_ui.update_health_bars()
        self.battle_ui.add_log_message("******************")

    def damage_calc(self, attack_type, is_max = False):
        self.battle_ui.add_log_message("Урон:")
        roll = 0
        if is_max:
            match attack_type:
                case AttackType.D4:
                    roll = 4
                case AttackType.D4x2:
                    roll = 8
                case AttackType.D6:
                    roll = 6
                case AttackType.D6x2:
                    roll = 12
            self.battle_ui.add_log_message(f"{roll}")
        else:
            match attack_type:
                case AttackType.D4:
                    roll = self.dice_system.d4()
                case AttackType.D4x2:
                    roll = self.dice_system.d4x2()
                case AttackType.D6:
                    roll = self.dice_system.d6()
                case AttackType.D6x2:
                    roll = self.dice_system.d6x2()
        return roll

    def crit_check(self, target):
        self.battle_ui.add_log_message("Проверка на критическое попадание:")
        roll = self.dice_system.d6x2()
        return roll >= target.armor