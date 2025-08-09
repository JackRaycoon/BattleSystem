from core.character import AttackType
import tkinter as tk
import asyncio


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
        self.print_in_log(f"Скорость {character.name}:")
        roll = self.dice_system.d6x2()
        character.battle_speed = character.speed + roll
        self.print_in_log(f"Итого: {character.speed} + {roll} = {character.battle_speed}")
        if character is self.player:
            self.prepare_to_fight(self.enemy)
        if (character is self.enemy) and (self.enemy.battle_speed > self.player.battle_speed):
            asyncio.run_coroutine_threadsafe(
                self.hit(False),
                self.battle_ui.loop
            )

    def print_in_log(self, message):
        self.battle_ui.add_log_message_sync(message)

    async def hit(self, is_first):
        if self.end_game:
            return

        #Whose turn?
        caster = self.player
        target = self.enemy
        if not is_first:
            caster = self.enemy
            target = self.player

        #Attack
        self.print_in_log(f"Ход {caster.name}:")
        roll = self.dice_system.d6()
        match roll:
            case x if x <= 2:
                self.print_in_log("Промах!")
            case x if x >=3:
                self.print_in_log("Попадание!")
                if self.crit_check(target):
                    self.print_in_log("Критический удар!")
                    dmg = self.damage_calc(caster.attack_type, True)
                else:
                    dmg = self.damage_calc(caster.attack_type)
                target.take_damage(dmg)
                self.battle_ui.update_health_bars()
        self.print_in_log("******************")

        #Check end of game
        if target.is_dead():
            self.end_game = True
            self.print_in_log(f"{caster.name} победил!")
            self.battle_ui.attack_button.config(state=tk.DISABLED)
            return

        #Enemy turn
        if is_first:
            asyncio.run_coroutine_threadsafe(
                self.hit(False),
                self.battle_ui.loop
            )
        #Unlock Atk Btn
        else:
            while not await self.battle_ui.is_queue_empty():
                await asyncio.sleep(0.1)

            self.battle_ui.root.after(0, lambda: self.battle_ui.attack_button.config(state=tk.NORMAL))

    def damage_calc(self, attack_type, is_max = False):
        self.print_in_log("Урон:")
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
            self.print_in_log(f"{roll}")
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
        self.print_in_log("Проверка на критическое попадание:")
        roll = self.dice_system.d6x2()
        return roll >= target.armor