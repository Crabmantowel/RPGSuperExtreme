import tkinter as tk
from tkinter import ttk

import sqlite3
from sqlite3 import Error

# from random import randint, randrange

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
        tk.Tk.resizable(self, width=False, height=False)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for one_of_frames in (Main_menu, New_game, Load_game, Statistics, Options, New_hero, Load_hero):  # A tuple of frames in our app, don`t forget to update if new ones, added
            frame = one_of_frames(container, self)
            self.frames[one_of_frames] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(Main_menu)

    def show_frame(self, container):

        frame = self.frames[container]
        frame.tkraise()


class Main_menu(tk.Frame):

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
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Character Creator", font=TYPIC_FONT)
        label.grid(row=0, column=5)

        toolbar = tk.Listbox(self, bg="#e0e0eb", selectmode='SINGLE')

        try:
            sql_connector = sqlite3.connect('RPGSE.db')
            sql_cursor = sql_connector.cursor()
        except Error as e:
            print(e)
        sql_cursor.execute("""SELECT * FROM Races""")
        list_of_races = sql_cursor.fetchall()
        race_number = 0
        for race in list_of_races:
            toolbar.insert(race_number, list_of_races[race_number][1])
            race_number += 1
        toolbar.grid(row=1, column=0, sticky="ns")

        rase_modifier_label = ttk.Label(self, text="FILLER", font=TYPIC_FONT)
        rase_modifier_label.grid(row=2, column=0)

        def get_player_stats(self):
            player_stats_list = [player_strength.get()]
            print(player_stats_list)

        player_strength = tk.Scale(self, orient=tk.HORIZONTAL, length=300, from_=0, to=10, tickinterval=10, resolution=1)
        player_strength.grid(row=1, column=5)

        apply_stats_button = ttk.Button(self, text=u"Apply Stats")
        apply_stats_button.bind("<Button-1>", get_player_stats)  # Why there`s a need to bind it?! Without binding it`s not working
        apply_stats_button.grid(row=6, column=6)

        nh_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame(New_game))
        nh_back.grid(row=10, column=5)


class Load_hero(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Choose a Character", font=TYPIC_FONT)
        label.pack(pady=5, padx=10)

        lh_back = ttk.Button(self, text="Back", command=lambda: controller.show_frame(New_game))
        lh_back.pack()


class Load_game(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Load Game", font=MAIN_MENU_FONT)
        label.pack(pady=10, padx=10)

        lg_main_menu_button = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(Main_menu))
        lg_main_menu_button.pack()


class Statistics(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Statistics", font=MAIN_MENU_FONT)
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

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Options", font=MAIN_MENU_FONT)
        label.grid(row=0, column=0)

        window_resolution_label = ttk.Label(self, text="Window Resolution")
        window_resolution_label.grid(row=1, column=0)

        window_resolution_option = ttk.Combobox(self, text="Window Resolution", width=50, state="readonly")
        window_resolution_option["values"] = RESOLUTION_LIST
        # window_resolution_option.current(1)
        window_resolution_option.grid(row=1, column=1)

        def current_window_resolution(self):
            value_now = window_resolution_option.get()
            print("Resolution is", value_now)

        apply_resolution_button = ttk.Button(self, text=u"Apply")
        apply_resolution_button.grid(row=1, column=2)
        apply_resolution_button.bind("<Button-1>", current_window_resolution)  # Why it must be only <Button-1>?!

        stat_main_menu_button = ttk.Button(self, text="Main Menu", command=lambda: controller.show_frame(Main_menu))
        stat_main_menu_button.grid(row=10, column=0, sticky="sew")


game = RPGSE()
game.mainloop()
