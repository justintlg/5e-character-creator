#!/usr/bin/python3

"""This is a 5e player character creation assistant"""

import random
import requests as req
import tkinter as tk
from tkinter import ttk

def race_API():
    """This function generates a list of playable races from the PHB"""
    API = "https://www.dnd5eapi.co/api/races/"
#grabs races dictionary from API gets value for key:results, which is a list of dictionaries
    dict = req.get(API).json()['results']
#remainder grabs value for key:name in every dictionary of list from results and makes a new list of those values and returns that list for later use
    name = 'name'
    races = ['Other']
    for species in dict:
        races.append(species[name])
    return races

def class_API():
    """This function generates a list of playable classes from the PHB"""
    API = "https://www.dnd5eapi.co/api/classes/"
#grabs classes dictionary from API gets value for key:results, which is a list of dictionaries
    dict = req.get(API).json()['results']
#remainder grabs value for key:name in every dictionary of list from results and makes a new list of those values and returns that list for later use
    name = 'name'
    classes = ['Other']
    for type in dict:
        classes.append(type[name])
    return classes     

#def background_API():
    #"""This function should generate a list of backgrounds from the PHB but is a work in progress"""
    #API = "https://www.dnd5eapi.co/api/backgrounds"
    #dict = req.get(API).json()['results']
    #name = 'name'
    #backgrounds = ['Other']
    #for type in dict:
    #    backgrounds.append(type[name])
    #return backgrounds


def rollmydice():
    """This function rolls 4d6 and then drops the lowest roll"""
    count = 0
    pre_drop = []
    while count < 4:
        pre_drop.append(random.randint(1,6))
        count += 1
    arranged = sorted(pre_drop, reverse= True)
    arranged.pop()
    final = sum(arranged)
    return final

def your_stats(event):
    stats_selected.config(text= f'You selected {chosen_method.get()}\n{ability_scores()}')

def ability_scores():
    """This function will help the user determine their ability scores/stats"""
#these are lists containing ability scores to be used
    std_array = [15, 14, 13, 12, 10, 8]
    rolled_stats = []
    if chosen_method.get() == 'Standard Array':
        return f'Your pre-bonus stats are\n{std_array}'
#this uses a predefined function to roll 4d6 and drop the lowest 6 times and arranges them into a list
    elif chosen_method.get() == 'Rolling':
        count = 0
        rolls = []
        while count < 6:
            rolls.append(rollmydice())
            count += 1
        rolled_stats = sorted(rolls, reverse= True)
        return f'Your pre-bonus stats are\n{rolled_stats}'
    #elif chosen_method.get() == 'Point-Buy':
    elif chosen_method.get() == 'Other':
        return 'This means you and your DM/GM will figure out your stats some other way'



def app_window():
    """This function creates the window to gather information and help the user get started with character creation!!"""
#allows modification of these variables at the global level rather than just in this function
    global chosen_class, chosen_race, chosen_background, chosen_method, chosen_align1, chosen_align2, stats_selected
#creates main app window
    root = tk.Tk()
#sets window title
    root.title('Character Creator')
#sets window size
    root.geometry('800x500')
#creates tkinter string variables
    chosen_class = tk.StringVar()
    chosen_race = tk.StringVar()
    chosen_background = tk.StringVar()
    chosen_method = tk.StringVar()
    chosen_align1 = tk.StringVar()
    chosen_align2 = tk.StringVar()
    #stats = tk.StringVar()
#Headline
    label = tk.Label(root, text = "Let's make this character", font= ('Georgia', 26))
    label.pack(anchor='center')
#create frames for placing widgets in desired locations
    frame1 = tk.Frame()
    frame1.pack(side= 'left')
    frame2 = tk.Frame()
    frame2.pack(side= 'right')
    frame3 = tk.Frame()
    frame3.pack(anchor= 'center')
#ask for desired class
    class_lbl = tk.Label(frame1, text= 'What Class would you like to play?')
    class_lbl.pack()
    class_options = ttk.Combobox(frame1, values = class_API(), textvariable= chosen_class)
    class_options.set('select a class')
    class_options.pack()
#ask what race
    race_lbl = tk.Label(frame1, text= 'What Race is your character?')
    race_lbl.pack()
    race_options = ttk.Combobox(frame1, values= race_API(), textvariable= chosen_race)
    race_options.set('select a race')
    race_options.pack()
#ask what background
    background_lbl = tk.Label(frame1, text= 'What is your character background?')
    background_lbl.pack()
    backgrounds = ['Work in progress']
    background_options = ttk.Combobox(frame1, values= backgrounds, textvariable= chosen_background)
    background_options.set('Work in progress')
    background_options.pack()
#ask the user for their alignment
    align_lbl = tk.Label(frame1, text= 'What is your alignment?\nSelect one of each.')
    align_lbl.pack()
    align_law = ['Lawful ', 'Neutral ', 'Chaotic ']
    align_opt1 = ttk.Combobox(frame1, values= align_law, textvariable= chosen_align1)
    align_opt1.set('choose 1')
    align_opt1.pack()
    align_good = ['Good', 'Neutral', 'Evil']
    align_opt2 = ttk.Combobox(frame1, values= align_good, textvariable= chosen_align2)
    align_opt2.set('choose 1')
    align_opt2.pack()
#ask how they would like to determine their stats
    stats_lbl = tk.Label(frame1, text= 'How will you determine your stats?')
    stats_lbl.pack()
    stats_method = ['Other', 'Rolling', 'Point-Buy', 'Standard Array']
    stats_options = ttk.Combobox(frame1, values= stats_method, textvariable= chosen_method)
    stats_options.set('select a method')
    stats_options.pack()
#determining the user stats/ability scores
    scores_lbl = tk.Label(frame3, text= 'Lets assign your stats', font= 18)
    scores_lbl.pack()
#display current stat selection
    stats_selected = tk.Label(frame3, text= 'select a method for acquiring your stats')
    stats_selected.pack()
    stats_options.bind('<<ComboboxSelected>>', your_stats)
#a summary of the current state of the character
    char_sofar = tk.Label(frame2, text= 'Here is your character so far!')
    char_sofar.pack()
#waits for user interaction (event loop)
    root.mainloop()
app_window() 
