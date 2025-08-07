from enum import Enum, auto
class AttackType(Enum):
    D4 = auto()
    D4x2 = auto()
    D6 = auto()
    D6x2 = auto()

class Character:
    def __init__(self, name, hp, armor, attack_type, speed):
        self.name = name
        self.max_hp = hp
        self.current_hp = hp
        self.armor = armor
        self.attack_type = attack_type
        self.speed = speed
        self.battle_speed = 0

    def is_dead(self):
        return self.current_hp == 0

    def hp_percent(self):
        return round((self.current_hp / self.max_hp) * 100, 2)

    def attack_type_text(self):
        match self.attack_type:
            case AttackType.D4:
                 return "d4"
            case AttackType.D6:
                return "d6"
            case AttackType.D4x2:
                return "2d4"
            case AttackType.D6x2:
                return "2d6"
        return None

    def take_damage(self, damage):
        self.current_hp -= damage
        if self.current_hp <= 0:
            self.current_hp = 0

class Player(Character):
    def __init__(self):
        super().__init__("Григорий", 50, 8, AttackType.D4x2, 5)

class Enemy(Character):
    def __init__(self):
        super().__init__("Химера", 30, 7, AttackType.D4, 6)