import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os


class BattleUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Боевая система")
        self.root.geometry("800x600")

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.load_images()

        self.create_player_frames()
        self.create_log_frame()
        self.create_attack_button()

    def create_player_frames(self):
        self.player_frame = ttk.Frame(self.root, padding=10)
        self.player_frame.grid(row=0, column=0, sticky="nsew")

        self.enemy_frame = ttk.Frame(self.root, padding=10)
        self.enemy_frame.grid(row=0, column=2, sticky="nsew")

        self.fill_character_frame(self.player_frame, "Игрок", 75, 100)
        self.fill_character_frame(self.enemy_frame, "Противник", 50, 50, False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)

    def fill_character_frame(self, frame, name, hp_percent, armor, is_player = True):
        if is_player and hasattr(self, 'player_photo') and self.player_photo:
            img_label = ttk.Label(frame, image=self.player_photo)
        elif not is_player and hasattr(self, 'enemy_photo') and self.enemy_photo:
            img_label = ttk.Label(frame, image=self.enemy_photo)
        else:
            img_label = ttk.Label(frame, text="[Изображение персонажа]",
                                  background="lightgray", width=20, anchor="center")

        img_label.pack(pady=10)

        name_label = ttk.Label(frame, text=name, font=('Arial', 12, 'bold'))
        name_label.pack()

        hp_label = ttk.Label(frame, text="HP:")
        hp_label.pack(pady=(10, 0))

        hp_bar = ttk.Progressbar(frame, orient="horizontal",
                                 length=200, mode="determinate",
                                 value=hp_percent)
        hp_bar.pack()

        hp_value = ttk.Label(frame, text=f"{hp_percent}%")
        hp_value.pack()

        armor_label = ttk.Label(frame, text=f"Броня: {armor}", font=('Arial', 10))
        armor_label.pack(pady=(10, 0))

    def create_log_frame(self):
        self.log_frame = ttk.Frame(self.root, padding=10)
        self.log_frame.grid(row=0, column=1, sticky="nsew")

        self.log_text = tk.Text(self.log_frame, wrap="word", width=40,
                                height=20, state="disabled")
        scrollbar = ttk.Scrollbar(self.log_frame, orient="vertical",
                                  command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        self.add_log_message("Бой начался!")

    def create_attack_button(self):
        self.button_frame = ttk.Frame(self.root)
        self.button_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.attack_button = ttk.Button(self.button_frame, text="Атаковать", width=20)
        self.attack_button.pack()

    def add_log_message(self, message):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.configure(state="disabled")
        self.log_text.see("end")

    def load_images(self):
        self.player_image_path = "images/player.jpg"
        self.enemy_image_path = "images/enemy.jpg"

        try:
            player_img = Image.open(self.player_image_path)
            player_img = player_img.resize((150, 200), Image.LANCZOS)
            self.player_photo = ImageTk.PhotoImage(player_img)

            enemy_img = Image.open(self.enemy_image_path)
            enemy_img = enemy_img.resize((150, 200), Image.LANCZOS)
            self.enemy_photo = ImageTk.PhotoImage(enemy_img)

        except FileNotFoundError:
            self.player_photo = None
            self.enemy_photo = None

if __name__ == "__main__":
    root = tk.Tk()
    app = BattleUI(root)
    root.mainloop()