import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image

import sqlite3
from sqlite3 import Error

import random

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
matplotlib.use("TkAgg")

MAIN_MENU_FONT = ("Verdana", 12)
TYPIC_FONT = ("Verdana", 8)
RESOLUTION_LIST = ["320x200", "800x600", "1024x768", "1366x768"]


class RPGSE(tk.Tk):
    """RPG Super Extreme"""

    def __init__(self, *args, **kwargs):
        """Initializing frame"""

        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "RPG Super Extreme")
        tk.Tk.iconbitmap(self, default="Skelly.ico")  # Don`t work with .bmp or .png formats
        tk.Tk.geometry(self, "800x600")
        #tk.Tk.resizable(self, width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for one_of_frames in (Main_menu, New_game, Load_game, Statistics, Options, New_hero, Load_hero, Game):  # A tuple of frames in our app, don`t forget to update if new ones, added
            frame = one_of_frames(container, self)
            self.frames[one_of_frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main_menu)

    def show_frame(self, container):

        frame = self.frames[container]
        frame.tkraise()


class Main_menu(tk.Frame):
    ''''Game`s new menu'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Main Menu", font=MAIN_MENU_FONT)
        label.pack(pady=10, padx=10)

        mm_new_game_button = ttk.Button(self, text="New Game", command=lambda: controller.show_frame(New_game))
        mm_new_game_button.pack()
        mm_load_game_button = ttk.Button(self, text="Load Game", command=lambda: controller.show_frame(Load_game))
        mm_load_game_button.pack()
        mm_statistics_button = ttk.Button(self, text="Statistics", command=lambda: controller.show_frame(Statistics))
        mm_statistics_button.pack()
        mm_options = ttk.Button(self, text="Options", command=lambda: controller.show_frame(Options))
        mm_options.pack()


class New_game(tk.Frame):
    ''''Sub-menu for player to decide what to do next'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="New Game", font=MAIN_MENU_FONT)
        label.pack(pady=10, padx=10)

        ng_new_hero = ttk.Button(self, text="Create new hero", command=lambda: controller.show_frame(New_hero))
        ng_new_hero.pack()
        ng_premade_hero = ttk.Button(self, text="Load hero", command=lambda: controller.show_frame(Load_hero))
        ng_premade_hero.pack()
        ng_main_menu_button = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(Main_menu))
        ng_main_menu_button.pack()


class New_hero(tk.Frame):
    ''''Hero creation window'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        #Sub-Frames go here
        player_name_frame = tk.Frame(self, parent)
        player_name_frame.grid(row=1, column=1)
        race_frame = tk.Frame(self, parent)
        race_frame.grid(row=2, column=0)
        stats_frame = tk.Frame(self, parent)
        stats_frame.grid(row=2, column=1)
        stats_label = tk.Frame(self, parent)
        stats_label.grid(row=2, column=2)
        back_next_frame = tk.Frame(self, parent)
        back_next_frame.grid(row=10, column=3)
        label = ttk.Label(self, text="Character Creator", font=TYPIC_FONT)
        label.grid(row=0, column=0)

        wrong_names = open("Vulgar_names.txt", 'r')
        list_of_bad_names = wrong_names.read().split()

        def name_vulgarity_check():
            if player_name.get().lower() in list_of_bad_names:
                vulgar_name_error = tk.Label(player_name_frame, text="Try non-vulgar name", fg='red')
                vulgar_name_error.grid(row=1, column=1)
            else:
                welcome_label = tk.Label(player_name_frame, text=f"You`r new name is {player_name.get()}!", fg="green")
                welcome_label.grid(row=1, column=1)

        username_label = tk.Label(player_name_frame, text="Enter your username: ")
        username_label.grid(row=0, column=0)

        player_name = tk.Entry(player_name_frame, width=50)
        player_name.grid(row=0, column=1)

        button = ttk.Button(player_name_frame, text="Submit", command=name_vulgarity_check)
        button.grid(row=0, column=2)

        race_options = tk.Listbox(race_frame, bg="#e0e0eb", selectmode='SINGLE')
        try:
            sql_connector = sqlite3.connect('RPGSE.db')
            sql_cursor = sql_connector.cursor()
        except Error as e:
            print(e)
        sql_cursor.execute("""SELECT *
                                FROM Races;""")
        global list_of_races
        list_of_races = sql_cursor.fetchall()
        race_number = 0
        for race in list_of_races:
            race_options.insert(race_number, list_of_races[race_number][1])
            race_number += 1
        race_options.grid(row=0, column=0)

        def show_hp_description(race):
            sql_cursor.execute(f"""SELECT HP_modifier
                                    FROM Races
                                    WHERE Race_name = '{race}';""")
            return sql_cursor.fetchall()

        def pick_race(self):
            highlighted_race = race_options.get(race_options.curselection())
            chosen_race_var.set(highlighted_race)
            chosen_race_descriptor = tk.Message(race_frame, text=f"You`ve chosen a {highlighted_race}, it receives an hp boost of {show_hp_description(highlighted_race)[0][0]} hp")
            chosen_race_descriptor.grid(row=3, column=0)

        chosen_race_var = tk.StringVar()
        race_picker_label = tk.Label(race_frame, font=TYPIC_FONT, width=10, textvariable=chosen_race_var)
        race_picker_label.grid(row=1, column=0)

        race_pick_confirmation = tk.Button(race_frame, text="Pick race")
        race_pick_confirmation.bind("<Button-1>", pick_race)
        race_pick_confirmation.grid(row=2, column=0)

        def apply_player_stats(self):
            player_stats_list = [player_strength.get(),
                                 player_perception.get(),
                                 player_endurance.get(),
                                 player_charisma.get(),
                                 player_intelligence.get(),
                                 player_agility.get(),
                                 player_luck.get()
                                 ]
            print(player_stats_list)

        GIVEN_STAT_POINTS = tk.IntVar()

        def onScale(val):
            v = GIVEN_STAT_POINTS.get() + int(float(val))
            GIVEN_STAT_POINTS.set(v)

        def create_stats_scale(stat_name):
            stat_name = tk.Scale(stats_frame, orient=tk.HORIZONTAL, length=300, from_=0, to=10, tickinterval=10, resolution=1, width=5, label=stat_name, command=onScale)
            return stat_name

        player_strength = create_stats_scale("Strength")
        player_strength.grid(row=1, column=0)
        player_perception = create_stats_scale("Perception")
        player_perception.grid(row=2, column=0)
        player_endurance = create_stats_scale("Endurance")
        player_endurance.grid(row=3, column=0)
        player_charisma = create_stats_scale("Charisma")
        player_charisma.grid(row=4, column=0)
        player_intelligence = create_stats_scale("Intelligence")
        player_intelligence.grid(row=5, column=0)
        player_agility = create_stats_scale("Agility")
        player_agility.grid(row=6, column=0)
        player_luck = create_stats_scale("Luck")
        player_luck.grid(row=7, column=0)

        #THIS PART IS UNDER CONSTRUCTION! IT DOESN`T WORK AS INTENDED
        # stat_points_counter = tk.Label(stats_frame, font=MAIN_MENU_FONT, textvariable=GIVEN_STAT_POINTS)
        # stat_points_counter.grid(row=0, column=0)

        apply_stats_button = ttk.Button(stats_frame, text=u"Apply Stats")
        apply_stats_button.bind("<Button-1>", apply_player_stats)  # Why there`s a need to bind it?! Without binding it`s not working
        apply_stats_button.grid(row=8, column=0)

        nh_back = ttk.Button(back_next_frame, text="Back", command=lambda: controller.show_frame(New_game))
        nh_back.grid(row=0, column=0)
        nh_next = ttk.Button(back_next_frame, text="Next", command=lambda: controller.show_frame(Game))
        nh_next.grid(row=0, column=1)


class Load_hero(tk.Frame):
    '''If there was a premade character or player created a new one, player can load it with all stats'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Choose a Character: UNDER CONSTRUCTION!", font=MAIN_MENU_FONT)
        label.pack(pady=5, padx=10)

        lh_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame(New_game))
        lh_back.pack()


class Load_game(tk.Frame):
    ''''Loads the game'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Load Game: UNDER CONSTRUCTION!", font=MAIN_MENU_FONT)
        label.pack(pady=10, padx=10)

        lg_main_menu_button = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(Main_menu))
        lg_main_menu_button.pack()


class Statistics(tk.Frame):
    ''''Shows player statistics with a graph'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Statistics: UNDER CONSTRUCTION", font=MAIN_MENU_FONT)
        label.pack(pady=10, padx=10)

        stat_main_menu_button = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(Main_menu))
        stat_main_menu_button.pack()

        f = Figure(figsize=(5, 5), dpi=100)  # f stands for Figure
        a = f.add_subplot(111)
        a.plot([1, 2, 3, 4, 5, 6, 7, 8], [5, 1, 3, 6, 4, 7, 8, 9])  # first one is for x axis, second - y, x&y must correlate on the quantity of inputs

        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)


class Options(tk.Frame):
    '''Frame for options change'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Options", font=MAIN_MENU_FONT)
        label.grid(row=0, column=0)

        window_resolution_label = ttk.Label(self, text="Window Resolution")
        window_resolution_label.grid(row=1, column=0)

        window_resolution_option = ttk.Combobox(self, text="Window Resolution", width=50, state="readonly")
        window_resolution_option["values"] = RESOLUTION_LIST
        window_resolution_option.current(1)
        window_resolution_option.grid(row=1, column=1)

        def current_window_resolution(self):
            global value_now
            value_now = window_resolution_option.get()
            print("Resolution is", value_now)
            return value_now

        apply_resolution_button = ttk.Button(self, text=u"Apply")
        apply_resolution_button.grid(row=1, column=2)
        apply_resolution_button.bind("<Button-1>", current_window_resolution)  # Why it must be only <Button-1>?!

        stat_main_menu_button = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(Main_menu))
        stat_main_menu_button.grid(row=10, column=0, sticky="sew")


class Game(tk.Frame):
    ''''The game itself'''
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        name_health_bar_frame = tk.Frame(self, parent, bg="Green")
        name_health_bar_frame.grid(row=0, column=0)

        health_icon = ImageTk.PhotoImage(Image.open("Health.png"))
        player_health_label = tk.Label(name_health_bar_frame, image=health_icon, text="HEALTH")
        player_health_label.grid(row=0, column=0)

        player_main_stats = tk.Message(name_health_bar_frame)
        player_main_stats.grid(row=0, column=1)

        fighting_frame = tk.Frame(self, parent, bg="Red")
        fighting_frame.grid(row=1, column=0, columnspan=4)

        player_fighting_frame = tk.Frame(fighting_frame, parent)
        player_fighting_frame.grid(row=0, column=0, columnspan=2)

        sword_img = tk.PhotoImage(file="Attack.png")
        player_attack_label = tk.Label(player_fighting_frame, image=sword_img)
        player_attack_label.grid(row=0, column=0)
        player_attack_button = tk.Button(player_fighting_frame, text="Attack")
        player_attack_button.grid(row=0, column=1)

        shield_img = tk.PhotoImage(file="Shield.png")
        player_defence_label = tk.Label(player_fighting_frame, image=shield_img)
        player_defence_label.grid(row=1, column=0)
        player_defence_button = tk.Button(player_fighting_frame, text="Defend")
        player_defence_button.grid(row=1, column=1)

        run_img = tk.PhotoImage(file="Run.png")
        player_run_label = tk.Label(player_fighting_frame, image=run_img)
        player_run_label.grid(row=2, column=0)
        player_run_button = tk.Button(player_fighting_frame, text="Run away")
        player_run_button.grid(row=2, column=1)

        enemy_fighting_frame = tk.Frame(fighting_frame, parent)
        enemy_fighting_frame.grid(row=0, column=2, columnspan=2)

        def enemy_encounter():
            enemy_encounter_label = tk.Message(enemy_fighting_frame, text=f"You`ve encountered a {random.choice(list_of_races[1])}")
            enemy_encounter_label.grid(row=0, column=0)

        lower_menu_frame = tk.Frame(self, parent, bg="Blue")
        lower_menu_frame.grid(row=2, column=0)
        game_main_menu_button = ttk.Button(lower_menu_frame, text="Return to main Menu", command=lambda: controller.show_frame(Main_menu))
        game_main_menu_button.grid(row=10, column=5)


game = RPGSE()
game.mainloop()
