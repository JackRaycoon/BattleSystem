from enum import Enum, auto
class AttackType(Enum):
    D4 = auto()
    D4x2 = auto()
    D6 = auto()
    D6x2 = auto()

class Character:
    def __init__(self, name, hp, armor, attack_type):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.armor = armor
        self.attack_type = attack_type

    def hp_percent(self):
        return round((self.current_hp / self.max_hp) * 100, 2)

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0

class Player(Character):
    def __init__(self):
        super().__init__("Игрок", 50, 8, AttackType.D4x2)

class Enemy(Character):
    def __init__(self):
        super().__init__("Химера", 30, 6, AttackType.D4)