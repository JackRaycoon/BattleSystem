from core.character import AttackType


class BattleCore:
    def __init__(self, dice_system):
        self.player = None
        self.enemy = None
        self.battle_ui = None
        self.end_game = False
        self.dice_system = dice_system
        self.init_characters()

    def init_characters(self):
        from core.character import Player, Enemy
        self.player = Player()
        self.enemy = Enemy()

    def prepare_to_fight(self, character):
        #Speed system
        self.battle_ui.add_log_message(f"Скорость {character.name}:")
        roll = self.dice_system.d6x2()
        character.battle_speed = character.speed + roll
        self.battle_ui.add_log_message(f"Итого: {character.speed} + {roll} = {character.battle_speed}")
        if character is self.player:
            self.prepare_to_fight(self.enemy)
        if (character is self.enemy) and (self.enemy.battle_speed > self.player.battle_speed):
            self.hit(False)


    def hit(self, is_first):
        if self.end_game:
            return

        #Whose turn?
        caster = self.player
        target = self.enemy
        if not is_first:
            caster = self.enemy
            target = self.player

        #Attack
        self.battle_ui.add_log_message(f"Ход {caster.name}:")
        roll = self.dice_system.d6()
        match roll:
            case x if x <= 2:
               self.battle_ui.add_log_message("Промах!")
            case x if x >=3:
                self.battle_ui.add_log_message("Попадание!")
                if self.crit_check(target):
                    self.battle_ui.add_log_message("Критический удар!")
                    dmg = self.damage_calc(caster.attack_type, True)
                else:
                    dmg = self.damage_calc(caster.attack_type)
                target.take_damage(dmg)
                self.battle_ui.update_health_bars()
        self.battle_ui.add_log_message("******************")

        #Check end of game
        if target.is_dead():
            self.end_game = True
            self.battle_ui.add_log_message(f"{caster.name} победил!")

        #Enemy turn
        if is_first:
            self.hit(False)

    def damage_calc(self, attack_type, is_max = False):
        self.battle_ui.add_log_message("Урон:")
        roll = 0

        if is_max: #Crit damage (max value)
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
        else: #Common damage calculation
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