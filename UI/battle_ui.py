import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import asyncio
import threading


class BattleUI:
    def __init__(self, root, battle_core):
        self.root = root
        self.root.title("Боевая система")
        self.root.geometry("800x600")

        self.battle_core = battle_core

        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.player_photo = None
        self.enemy_photo = None
        self.load_images()

        self.player_hp_bar = None
        self.enemy_hp_bar = None
        self.player_hp_label = None
        self.enemy_hp_label = None
        self.create_player_frames()

        self.log_frame = None
        self.log_text = None
        self.create_log_frame()

        self.attack_button = None
        self.create_attack_button()

        self.running = True
        self.loop = asyncio.new_event_loop()
        asyncio_thread = threading.Thread(target=self.run_async, daemon=True)
        asyncio_thread.start()

        self.message_queue = asyncio.Queue()
        self._queue_not_empty = asyncio.Event()
        self.log_task = None
        self.start_log_processor()

        self.add_log_message_sync("Бой начался!")

    async def process_log_messages(self):
        while True:
            message = await self.message_queue.get()
            self._queue_not_empty.set()
            self.log_text.configure(state="normal")
            self.log_text.insert("end", message + "\n")
            self.log_text.configure(state="disabled")
            self.log_text.see("end")
            await asyncio.sleep(0.5)
            if self.message_queue.empty():
                self._queue_not_empty.clear()
                self._update_attack_button_state()

    def _update_attack_button_state(self):
        def update():
            should_disable = self._queue_not_empty.is_set() or self.battle_core.end_game
            state = tk.NORMAL if not should_disable else tk.DISABLED
            self.attack_button.config(state=state)

        self.root.after(0, update)

    def start_log_processor(self):
        self.log_task = asyncio.run_coroutine_threadsafe(
            self.process_log_messages(),
            self.loop
        )

    async def add_log_message(self, message):
        self.attack_button.config(state=tk.DISABLED)
        await self.message_queue.put(message)

    def add_log_message_sync(self, message):
        asyncio.run_coroutine_threadsafe(
            self.add_log_message(message),
            self.loop
        )

    async def is_queue_empty(self):
        await asyncio.sleep(0.1)
        return self.message_queue.empty()

    def run_async(self):
        asyncio.set_event_loop(self.loop)
        while self.running:
            self.loop.run_until_complete(asyncio.sleep(0.1))

    def create_player_frames(self):
        player_frame = ttk.Frame(self.root, padding=10)
        player_frame.grid(row=0, column=0, sticky="nsew")

        enemy_frame = ttk.Frame(self.root, padding=10)
        enemy_frame.grid(row=0, column=2, sticky="nsew")

        player = self.battle_core.player
        enemy = self.battle_core.enemy
        self.fill_character_frame(player_frame, player)
        self.fill_character_frame(enemy_frame, enemy,False)

        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=0)
        self.root.columnconfigure(2, weight=1)
        self.root.rowconfigure(0, weight=1)

    def fill_character_frame(self, frame, character, is_player = True):
        if is_player and self.player_photo:
            img_label = ttk.Label(frame, image=self.player_photo)
        elif not is_player and self.enemy_photo:
            img_label = ttk.Label(frame, image=self.enemy_photo)
        else:
            img_label = ttk.Label(
                frame,
                text="[Изображение персонажа]",
                background="lightgray",
                width=20,
                anchor="center")

        img_label.pack(pady=10)

        name_label = ttk.Label(
            frame,
            text=character.name,
            font=('Arial', 12, 'bold'))
        name_label.pack()

        hp_label = ttk.Label(frame, text="HP:")
        hp_label.pack(pady=(10, 0))

        hp_bar = ttk.Progressbar(
            frame,
            orient="horizontal",
            length=200,
            mode="determinate",
            value=character.hp_percent())
        hp_bar.pack()

        if is_player:
            self.player_hp_bar = hp_bar
            self.player_hp_label = ttk.Label(frame,
                                             text=f"{character.current_hp}/{character.max_hp}"
                                                  f"({character.hp_percent()}%)")
        else:
            self.enemy_hp_bar = hp_bar
            self.enemy_hp_label = ttk.Label(frame,
                                            text=f"{character.current_hp}/{character.max_hp}"
                                                 f"({character.hp_percent()}%)")

        hp_label = self.player_hp_label if is_player else self.enemy_hp_label
        hp_label.pack()

        attack_type_label = ttk.Label(
            frame,
            text=f"Атака: {character.attack_type_text()}",
            font=('Arial', 10))
        attack_type_label.pack(pady=(10, 0))

        armor_label = ttk.Label(
            frame,
            text=f"Броня: {character.armor}",
            font=('Arial', 10))
        armor_label.pack(pady=(5, 0))

    def update_health_bars(self):
        player = self.battle_core.player
        player_hp = player.hp_percent()
        self.player_hp_bar['value'] = player_hp
        self.player_hp_label['text'] = f"{player.current_hp}/{player.max_hp} ({player_hp}%)"

        enemy = self.battle_core.enemy
        enemy_hp = enemy.hp_percent()
        self.enemy_hp_bar['value'] = enemy_hp
        self.enemy_hp_label['text'] = f"{enemy.current_hp}/{enemy.max_hp} ({enemy_hp}%)"

        self.root.update_idletasks()

    def create_log_frame(self):
        self.log_frame = ttk.Frame(self.root, padding=10)
        self.log_frame.grid(row=0, column=1, sticky="nsew")

        self.log_text = tk.Text(
            self.log_frame,
            wrap="word",
            width=40,
            height=20,
            state="disabled")
        scrollbar = ttk.Scrollbar(
            self.log_frame,
            orient="vertical",
            command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=scrollbar.set)

        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def create_attack_button(self):
        button_frame = ttk.Frame(self.root)
        button_frame.grid(row=1, column=0, columnspan=3, pady=10)

        self.attack_button = ttk.Button(
            button_frame,
            text="Атаковать",
            width=20,
            command=lambda: asyncio.run_coroutine_threadsafe(
            self.battle_core.hit(True),
            self.loop
        )
        )
        self.attack_button.pack()

    def load_images(self):
        from pathlib import Path

        current_dir = Path(__file__).parent
        images_dir = current_dir.parent / "images"

        player_image_path = images_dir / "player.jpg"
        enemy_image_path = images_dir / "enemy.jpg"

        try:
            player_img = Image.open(player_image_path)
            player_img = player_img.resize((150, 200), Image.LANCZOS)
            self.player_photo = ImageTk.PhotoImage(player_img)

            enemy_img = Image.open(enemy_image_path)
            enemy_img = enemy_img.resize((150, 200), Image.LANCZOS)
            self.enemy_photo = ImageTk.PhotoImage(enemy_img)

        except FileNotFoundError as e:
            print(f"Ошибка загрузки изображений: {e}")
            self.player_photo = None
            self.enemy_photo = None

    def __del__(self):
        self.running = False