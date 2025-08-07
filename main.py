import tkinter as tk
from UI.battle_ui import BattleUI
from core.battle_core import BattleCore
from core.dice_system import DiceSystem


def main():
    root = tk.Tk()
    dice_system = DiceSystem()
    battle_core = BattleCore(dice_system)
    app = BattleUI(root, battle_core)
    dice_system.battle_ui = app
    battle_core.battle_ui = app
    battle_core.prepare_to_fight(battle_core.player)
    root.mainloop()

if __name__ == "__main__":
    main()