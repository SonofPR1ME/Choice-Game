# Planning:

# The entire "happening" variable has completely broken combat and I now need to rewrite every function that includes it to modify
#       it in the whole code, which is like 15 functions, have mercy upon my soul   X
# Combat System   X
# Fix weird code formatting   X
# Play Again Option   X
# Reword the fortunes   X
# Stat Formatting   X
# Contamination/Cure System   X
# Blindness System   X
# Rerolling/Fortune Swaps   X
# Mass increase/decrease of stats   X
# Shopping System   X
# Chance System   X
# Square Change   X
# Screen Clearing   X
# PvP   X
# Multiple Real Players   X
# Personal Stat Changes   X
# Show active players stats during PvP and Shops   X
# More Randomness in PvP   X
# See other boards and stats once win condition is met   X
# Allow other players to uncontaminate each other in singleplayer   X
# Elements
# Classes?
# Abilities?
       # Square Swap
       # Rerolls
       # Glance at a blinded square
       # Shield (Doesn't apply to chance)
       # Saved cure
       # Unblind for a turn
       # Sabotage
       # Steal
       # Expose Squares
       # Expose Stats
       # Second Life
       # Half Pricing Card
       # Point Surge
# Square Explainations
# Traps?
# Boss Fights?
# Actual Ui
# Goal Generation?
# More/Less Players


# Time Spent Working on project:

# Sprint 6:

# June 30 (Tuesday): 1 hour; Made it so other players can all unconataminate each other in Singleplayer.
# July 2 (Thursday) 1 hour; Just neatified my code and fixed a minor, nearly unnoticable bug in the blindness system. Also made some
#      elements, though we will see if they get used.


import random
import os
import statistics

HEALTH_KEY = "Health"
STRENGTH_KEY = "Strength"
GOLD_KEY = "Gold"
POINTS_KEY = "Points"

RED_OPTIONS = ["Is Contaminated", "Loses 1 Gold", "Loses 1 Point", "Loses 1 Strength", 
              "Loses 1 Life", "Loses 3 Gold", "Loses 3 Strength", "Loses 3 Life", "Is Blinded", 
              "Has Nothing Happen", "Enemies Min Increases", "Enemies Max Increases",
              "Has Good Fortune", "Has Chaotic Fortune", "Bad Fortune x2", "Mass stat loss"]

ORANGE_OPTIONS = ["Gains 1 Gold", "Is attempting to gain 1 Point", "Gains 1 Strength", "Gains 1 Life", 
              "Gains 3 Gold", "Gains 3 Strength", "Gains 3 Life", "Is Unblinding", 
              "Has Nothing Happen", "Is Cured", "Has Bad Fortune", "Has Chaotic Fortune", "Good Fortune x2", "Mass stat gain"]

PURPLE_OPTIONS = ["Enemies Max Decreases", "Enemies Min Decreases", 
              "Gains 3 Gold", "Loses 3 Gold", "Gains 3 Strength", "Loses 3 Strength", 
              "Loses 3 Life", "Gains 3 Life", "Has Bad Fortune", "Has Good Fortune",
              "Enemies Min Increases to Max", "Enemies Max Decreases to Min", 
              "Enemies Min Increases", "Enemies Max Increases", "Runs into an Encounter", "Is Blinded", 
              "Is Unblinding", "Loses 1 Point", "Is attempting to gain 1 Point", "Is Contaminated", 
              "Is Cured", "Triggers Chance", "Triggers Square Change", "Chaotic Fortune x2", "Mass stat gain", "Mass stat loss"]


CHANCE_TIME_AMOUNTS = [1, 3, 5, 10, "Half", "Equalizes", "Swaps"]

SQUARE_CHANGE_OPTIONS = ["Add", "Add", "Add", "Add", "Remove", "Remove", "Remove", "Remove", "Remove", "Remove", "Swap"]
SQUARE_TYPES = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜"]

ELEMENTS = ["Fire", "Water", "Earth", "Air", "Lightning", "Ice", "Metal", "Wood", "Light", "Dark", "Toxin", "Psychic", "Draconic", 
            "Grass", "Blood", "Sword", "Bow", "Curse", "Mystic"]

p1_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
p1_elements = []
p1_contamination = []
p1_blind = False

p2_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
p2_elements = []
p2_contamination = []
p2_blind = False

p3_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
p3_elements = []
p3_contamination = []
p3_blind = False

p4_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
p4_elements = []
p4_contamination = []
p4_blind = False

choice = None
current_player = p1_stats
current_player_number = 1

mode = None

lose = False
win = False

active_players = [1, 2, 3, 4]
winning_players = []
pvp_stats_list = []

happening = None
enemy_min = 1
enemy_max = 5
enemy_average = (enemy_min + enemy_max) / 2

p1_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p1_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p1_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p2_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p2_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p2_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p3_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p3_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p3_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p4_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p4_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
p4_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
       "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]

def game_reset():
       if mode == "S":
              p1_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p1_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p1_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p2_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p2_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p2_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p3_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p3_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p3_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p4_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p4_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
              p4_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛",]
       else:
              p1_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p1_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p1_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p2_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p2_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p2_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p3_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p3_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p3_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p4_1 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p4_2 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
              p4_3 = ["🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "🟦", "⬜","🟨", "🟪", "🟧", "🟥",
                     "🟩", "🟫", "⬛","🟨", "🟪", "🟧", "🟥", "🟩", "🟫", "⬛", "⚔️ "]
       return p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3

def random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3):
       if 0 in p1_contamination:
              p1_1r = "🟥"
       else:
              p1_1r = random.choice(p1_1)
       if 1 in p1_contamination:
              p1_2r = "🟥"
       else:
              p1_2r = random.choice(p1_2)
       if 2 in p1_contamination:
              p1_3r = "🟥"
       else:
              p1_3r = random.choice(p1_3)
       if p1_blind == True:
              p1_1r = "➖"
              p1_2r = "➖"
              p1_3r = "➖"
       
       if 0 in p2_contamination:
              p2_1r = "🟥"
       else:
              p2_1r = random.choice(p2_1)
       if 1 in p2_contamination:
              p2_2r = "🟥"
       else:
              p2_2r = random.choice(p2_2)
       if 2 in p2_contamination:
              p2_3r = "🟥"
       else:
              p2_3r = random.choice(p2_3)
       if p2_blind == True:
              p2_1r = "➖"
              p2_2r = "➖"
              p2_3r = "➖"

       if 0 in p3_contamination:
              p3_1r = "🟥"
       else:
              p3_1r = random.choice(p3_1)
       if 1 in p3_contamination:
              p3_2r = "🟥"
       else:
              p3_2r = random.choice(p3_2)
       if 2 in p3_contamination:
              p3_3r = "🟥"
       else:
              p3_3r = random.choice(p3_3)
       if p3_blind == True:
              p3_1r = "➖"
              p3_2r = "➖"
              p3_3r = "➖"

       if 0 in p4_contamination:
              p4_1r = "🟥"
       else:
              p4_1r = random.choice(p4_1)
       if 1 in p4_contamination:
              p4_2r = "🟥"
       else:
              p4_2r = random.choice(p4_2)
       if 2 in p4_contamination:
              p4_3r = "🟥"
       else:
              p4_3r = random.choice(p4_3)
       if p4_blind == True:
              p4_1r = "➖"
              p4_2r = "➖"
              p4_3r = "➖"

       return p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r

def big_board(p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r):
       if 1 not in active_players:
              p1_1r = "❌"
              p1_2r = "❌"
              p1_3r = "❌"
       if 2 not in active_players:
              p2_1r = "❌"
              p2_2r = "❌"
              p2_3r = "❌"
       if 3 not in active_players:
              p3_1r = "❌"
              p3_2r = "❌"
              p3_3r = "❌"
       if 4 not in active_players:
              p4_1r = "❌"
              p4_2r = "❌"
              p4_3r = "❌"
       print (f"{p1_1r} {p1_2r} {p1_3r} | {p2_1r} {p2_2r} {p2_3r}\n-------------------\n{p3_1r} {p3_2r} {p3_3r} | {p4_1r} {p4_2r} {p4_3r}")

def choices(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3):
       global p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r, current_player_number, current_player, choice
       os.system('cls' if os.name == 'nt' else 'clear')
       stats()
       print()
       print (f"{p1_1r} {p1_2r} {p1_3r} | {p2_1r} {p2_2r} {p2_3r}\n-------------------\n{p3_1r} {p3_2r} {p3_3r} | {p4_1r} {p4_2r} {p4_3r}")
       validChoice = False
       while validChoice == False:
              choice = input("Please select 1-3 or 'L' to see your square list: ")
              choice = int(choice) if choice.isdigit() else choice
              if choice == 1:
                     current_player_number = 1
                     current_player = p1_stats
                     print()
                     print("Player 1")
                     action(p1_1r)
                     current_player_number = 2
                     current_player = p2_stats
                     print()
                     print("Player 2")
                     action(p2_1r)
                     current_player_number = 3
                     current_player = p3_stats
                     print()
                     print("Player 3")
                     action(p3_1r)
                     current_player_number = 4
                     current_player = p4_stats
                     print()
                     print("Player 4")
                     action(p4_1r)
                     validChoice = True
                     lose_and_win_check()
                     p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
              elif choice == 2:
                     current_player_number = 1
                     current_player = p1_stats
                     print()
                     print("Player 1")
                     action(p1_2r)
                     current_player_number = 2
                     current_player = p2_stats
                     print()
                     print("Player 2")
                     action(p2_2r)
                     current_player_number = 3
                     current_player = p3_stats
                     print()
                     print("Player 3")
                     action(p3_2r)
                     current_player_number = 4
                     current_player = p4_stats
                     print()
                     print("Player 4")
                     action(p4_2r)
                     validChoice = True
                     lose_and_win_check()
                     p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
              elif choice == 3:
                     current_player_number = 1
                     current_player = p1_stats
                     print()
                     print("Player 1")
                     action(p1_3r)
                     current_player_number = 2
                     current_player = p2_stats
                     print()
                     print("Player 2")
                     action(p2_3r)
                     current_player_number = 3
                     current_player = p3_stats
                     print()
                     print("Player 3")
                     action(p3_3r)
                     current_player_number = 4
                     current_player = p4_stats
                     print()
                     print("Player 4")
                     action(p4_3r)
                     validChoice = True
                     lose_and_win_check()
                     p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
              elif choice == "L" or choice == "l":
                     os.system('cls' if os.name == 'nt' else 'clear')
                     square_list()
                     validChoice = True
              elif choice == "healthybois":
                     p1_stats[HEALTH_KEY] += 100
                     p2_stats[HEALTH_KEY] += 100
                     p3_stats[HEALTH_KEY] += 100
                     p4_stats[HEALTH_KEY] += 100
                     print("Everyone's health has been increased by 100!")
              else:
                     print ("Bad input")
       print()
       input("Hit enter to continue")

def multi_choice(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3):
       global p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r, current_player_number
       global current_player, choice, active_players
       choice_vote = []
       validChoice = False
       for i in range(4):
              player = i + 1
              if player in active_players:
                     os.system('cls' if os.name == 'nt' else 'clear')
                     if player not in winning_players:
                            multi_stats(i)
                     else:
                            stats()
                     print()
                     if i == 0:
                            if 1 in winning_players:
                                   big_board(p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r)
                            else:
                                   print (f"{p1_1r} {p1_2r} {p1_3r}")
                     elif i == 1:
                            if 2 in winning_players:
                                   big_board(p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r)
                            else:
                                   print (f"{p2_1r} {p2_2r} {p2_3r}")
                     elif i == 2:
                            if 3 in winning_players:
                                   big_board(p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r)
                            else:
                                   print (f"{p3_1r} {p3_2r} {p3_3r}")
                     elif i == 3:
                            if 4 in winning_players:
                                   big_board(p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r)
                            else:
                                   print (f"{p4_1r} {p4_2r} {p4_3r}")
                     validChoice = False
                     while validChoice == False:
                            vote = input(f"Player {i + 1}, please select 1-3 or 'L' to see your square list: ")
                            vote = int(vote) if vote.isdigit() else vote
                            if isinstance(vote, int) and vote >= 1 and vote <= 3:
                                   choice_vote.append(vote)
                                   validChoice = True
                                   print()
                                   input("Hit enter to continue")
                            elif vote == "L" or vote == "l":
                                   os.system('cls' if os.name == 'nt' else 'clear')
                                   multi_square_list(i)
                                   os.system('cls' if os.name == 'nt' else 'clear')
                                   multi_stats(i)
                                   print()
                                   if i == 0:
                                          print (f"{p1_1r} {p1_2r} {p1_3r}")
                                   elif i == 1:
                                          print (f"{p2_1r} {p2_2r} {p2_3r}")
                                   elif i == 2:
                                          print (f"{p3_1r} {p3_2r} {p3_3r}")
                                   elif i == 3:
                                          print (f"{p4_1r} {p4_2r} {p4_3r}")
                            elif vote == "healthybois":
                                   p1_stats[HEALTH_KEY] += 100
                                   p2_stats[HEALTH_KEY] += 100
                                   p3_stats[HEALTH_KEY] += 100
                                   p4_stats[HEALTH_KEY] += 100
                                   print("Everyone's health has been increased by 100!")
                            else:
                                   print("Invalid input, please try again.")
       options = statistics.multimode(choice_vote)
       choice = random.choice(options)
       os.system('cls' if os.name == 'nt' else 'clear')
       print(f"The voted choice is square {choice}!")
       input("Hit enter to continue")
       if choice == 1:
              if 1 in active_players:
                     current_player_number = 1
                     current_player = p1_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 1")
                     print()
                     action(p1_1r)
                     input("Hit enter to continue")
              if 2 in active_players:
                     current_player_number = 2
                     current_player = p2_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 2")
                     print()
                     action(p2_1r)
                     input("Hit enter to continue")
              if 3 in active_players:
                     current_player_number = 3
                     current_player = p3_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 3")
                     print()
                     action(p3_1r)
                     input("Hit enter to continue")
              if 4 in active_players:
                     current_player_number = 4
                     current_player = p4_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 4")
                     print()
                     action(p4_1r)
                     input("Hit enter to continue")
              validChoice = True
              lose_and_win_check()
              p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
       elif choice == 2:
              if 1 in active_players:
                     current_player_number = 1
                     current_player = p1_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 1")
                     print()
                     action(p1_2r)
                     input("Hit enter to continue")
              if 2 in active_players:
                     current_player_number = 2
                     current_player = p2_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 2")
                     print()
                     action(p2_2r)
                     input("Hit enter to continue")
              if 3 in active_players:
                     current_player_number = 3
                     current_player = p3_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 3")
                     print()
                     action(p3_2r)
                     input("Hit enter to continue")
              if 4 in active_players:
                     current_player_number = 4
                     current_player = p4_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 4")
                     print()
                     action(p4_2r)
                     input("Hit enter to continue")
              validChoice = True
              lose_and_win_check()
              p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
       elif choice == 3:
              if 1 in active_players:
                     current_player_number = 1
                     current_player = p1_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 1")
                     print()
                     action(p1_3r)
                     input("Hit enter to continue")
              if 2 in active_players:
                     current_player_number = 2
                     current_player = p2_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 2")
                     print()
                     action(p2_3r)
                     input("Hit enter to continue")
              if 3 in active_players:
                     current_player_number = 3
                     current_player = p3_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 3")
                     print()
                     action(p3_3r)
                     input("Hit enter to continue")
              if 4 in active_players:
                     current_player_number = 4
                     current_player = p4_stats
                     os.system('cls' if os.name == 'nt' else 'clear')
                     print("Player 4")
                     print()
                     action(p4_3r)
                     input("Hit enter to continue")
              validChoice = True
              lose_and_win_check()
              p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)


def red():
       happening = random.choice(RED_OPTIONS)
       print(f"{happening}")
       stat_update(happening)
       
def orange():
       happening = random.choice(ORANGE_OPTIONS)
       print(f"{happening}")
       stat_update(happening)

def purple():
       happening = random.choice(PURPLE_OPTIONS)
       if happening == PURPLE_OPTIONS[14]:
              black()
       else:
              print(f"{happening}")
       stat_update(happening)

def shop():
       global current_player, current_player_number, p1_stats, p2_stats, p3_stats, p4_stats, mode
       if mode == "M":
              multi_stats(current_player_number - 1)
              print()
       happening = "Encounters a Merchant"
       print(f"{happening}")
       price1 = random.randint(1, 10)
       price2 = random.randint(1, 20)
       price3 = random.randint(1, 30)
       price4 = random.randint(10, 30)
       type1 = random.choice(["Health", "Strength", "Gold"])
       type2 = random.choice(["Health", "Strength", "Gold"])
       type3 = random.choice(["Health", "Strength", "Gold"])
       type4 = random.choice(["Health", "Strength", "Gold"])
       reward1 = random.randint(1, 10)
       reward2 = random.randint(1, 20)
       reward3 = random.randint(1, 30)
       reward4 = random.randint(1, 50)
       prices = [price1, price2, price3]

       print("Wares for Sale:")
       print(f"1. {reward1} {type1} for {price1} Gold")
       print(f"2. {reward2} {type2} for {price2} Gold")
       print(f"3. {reward3} {type3} for {price3} Gold")
       print(f"4. {reward4} {type4} for {price4} Health")
       if current_player[GOLD_KEY] < min(prices) and current_player[HEALTH_KEY] < price4:
              print("You cannot afford any of the items.")
       else:
              validChoice = False
              while validChoice == False:
                     choice = input("Please select 1-4: ")
                     choice = int(choice) if choice.isdigit() else choice
                     if choice == 1 and current_player[GOLD_KEY] >= price1:
                            current_player[GOLD_KEY] -= price1
                            current_player[type1] += reward1
                            print(f"You bought {reward1} {type1} for {price1} Gold!")
                            validChoice = True
                     elif choice == 2 and current_player[GOLD_KEY] >= price2:
                            current_player[GOLD_KEY] -= price2
                            current_player[type2] += reward2
                            print(f"You bought {reward2} {type2} for {price2} Gold!")
                            validChoice = True
                     elif choice == 3 and current_player[GOLD_KEY] >= price3:
                            current_player[GOLD_KEY] -= price3
                            current_player[type3] += reward3
                            print(f"You bought {reward3} {type3} for {price3} Gold!")
                            validChoice = True
                     elif choice == 4 and current_player[HEALTH_KEY] >= price4:
                            current_player[HEALTH_KEY] -= price4
                            current_player[type4] += reward4
                            print(f"You bought {reward4} {type4} for {price4} Health!")
                            validChoice = True
                     else:
                            print("Bad input or you cannot afford that item.")


def green():
       happening = "Is attempting to gain 1 Point"
       print(f"{happening}")
       stat_update(happening)

def brown():
       happening = "Has Nothing Happen"
       print(f"{happening}")
       stat_update(happening)
       
def black():
       happening = "End of Encounter"
       encounter()
       print(f"{happening}")

def square_change():
       global p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3
       happening = "Is changing their squares"
       print(f"{happening}")
       if current_player_number == 1:
              player_squares = [p1_1, p1_2, p1_3]
       elif current_player_number == 2:
              player_squares = [p2_1, p2_2, p2_3]
       elif current_player_number == 3:
              player_squares = [p3_1, p3_2, p3_3]
       elif current_player_number == 4:
              player_squares = [p4_1, p4_2, p4_3]
       position = random.randint(0, 2)
       square_type1 = random.choice(SQUARE_TYPES)
       square_type2 = random.choice(SQUARE_TYPES)
       change = random.choice(SQUARE_CHANGE_OPTIONS)
       square = player_squares[position]
       if change == "Add":
              print(f"Adding {square_type1} to square {position + 1}")
              square.append(square_type1)
       elif change == "Remove":
              if square_type1 in square:
                     print(f"Removing {square_type1} from square {position + 1}")
                     square.remove(square_type1)
              else:
                     print(f"{square_type1} is not in square {position + 1}, no change made.")
       elif change == "Swap":
              if square_type1 == square_type2:
                     print(f"Swap skipped because both swap types are {square_type1}")
              else:
                     print(f"Swapping amount of {square_type1} with amount of {square_type2} in square {position + 1}")
                     amount1 = square.count(square_type1)
                     amount2 = square.count(square_type2)
                     for i in range(amount1):
                            square.remove(square_type1)
                     for i in range(amount2):
                            square.remove(square_type2)
                     for i in range(amount1):
                            square.append(square_type2)
                     for i in range(amount2):
                            square.append(square_type1)
       loopDone = False
       while loopDone == False:
              chance = random.randint(1, 3)
              if chance == 3:
                     loopDone = True
              else:
                     position = random.randint(0, 2)
                     square_type1 = random.choice(SQUARE_TYPES)
                     square_type2 = random.choice(SQUARE_TYPES)
                     change = random.choice(SQUARE_CHANGE_OPTIONS)
                     square = player_squares[position]
                     if change == "Add":
                            print(f"Adding {square_type1} to square {position + 1}")
                            square.append(square_type1)
                     elif change == "Remove":
                            if square_type1 in square:
                                   print(f"Removing {square_type1} from square {position + 1}")
                                   square.remove(square_type1)
                            else:
                                   print(f"{square_type1} is not in square {position + 1}, no change made.")
                     elif change == "Swap":
                            if square_type1 == square_type2:
                                   print(f"Swap skipped because both swap types are {square_type1}")
                            else:
                                   print(f"Swapping amount of {square_type1} with amount of {square_type2} in square {position + 1}")
                                   amount1 = square.count(square_type1)
                                   amount2 = square.count(square_type2)
                                   for i in range(amount1):
                                          square.remove(square_type1)
                                   for i in range(amount2):
                                          square.remove(square_type2)
                                   for i in range(amount1):
                                          square.append(square_type2)
                                   for i in range(amount2):
                                          square.append(square_type1)
       
def chance():
       happening = "Chance Time!"
       print(f"{happening}")
       taker = random.randint(1, 4)
       type = random.choice(["Health", "Strength", "Gold", "Points"])
       amount = random.choice(CHANCE_TIME_AMOUNTS)
       giver = random.randint(1, 4)
       different_player = False
       while different_player == False:
              if giver == taker:
                     giver = random.randint(1, 4)
              else:
                     different_player = True
       if taker == 1:
              ptaker = p1_stats
       elif taker == 2:
              ptaker = p2_stats
       elif taker == 3:
              ptaker = p3_stats
       elif taker == 4:
              ptaker = p4_stats
       if giver == 1:
              pgiver = p1_stats
       elif giver == 2:
              pgiver = p2_stats
       elif giver == 3:
              pgiver = p3_stats
       elif giver == 4:
              pgiver = p4_stats
       
       if isinstance(amount, int):
              print(f"Player {taker} takes {amount} {type} from Player {giver}!")
              if type == "Health" or type == "Gold":
                     ptaker[type] += amount
                     pgiver[type] -= amount
              elif type == "Strength":
                     amountlost = None
                     if pgiver[type] < amount:
                            amountlost = pgiver[type]
                            pgiver[type] = 0
                     else:
                            amountlost = amount
                            pgiver[type] -= amount
                     ptaker[type] += amountlost
              elif type == "Points":
                     amountlost = None
                     if pgiver[type] < amount:
                            amountlost = pgiver[type]
                            pgiver[type] = 0
                     else:
                            amountlost = amount
                            pgiver[type] -= amount
                     if ptaker[type] + amountlost > 10:
                            ptaker[type] = 10
                     else:
                            ptaker[type] += amountlost
                     
       elif amount == "Half":
              print(f"Player {taker} takes half of Player {giver}'s {type}!")
              amountlost = pgiver[type] // 2
              if type == "Health" or type == "Gold" or type == "Strength":
                     pgiver[type] -= amountlost
                     ptaker[type] += amountlost

              elif type == "Points":
                     pgiver[type] -= amountlost
                     if ptaker[type] + amountlost > 10:
                            ptaker[type] = 10
                     else:
                            ptaker[type] += amountlost
       elif amount == "Equalizes":
              print(f"Player {taker} equalizes their {type} with Player {giver}!")

              average = (ptaker[type] + pgiver[type]) // 2
              ptaker[type] = average
              pgiver[type] = average
       elif amount == "Swaps":
              print(f"Player {taker} swaps their {type} with Player {giver}!")
              temp = ptaker[type]
              ptaker[type] = pgiver[type]
              pgiver[type] = temp
                     
def blind():
       global p1_blind, p2_blind, p3_blind, p4_blind, p1_contamination, p2_contamination, p3_contamination, p4_contamination
       choice_index = choice - 1
       if current_player_number == 1:
              if choice_index in p1_contamination:
                     red()
              else:
                     if choice_index == 0:
                            action(random.choice(p1_1))
                     elif choice_index == 1:
                            action(random.choice(p1_2))
                     elif choice_index == 2:
                            action(random.choice(p1_3))
       if current_player_number == 2:
              if choice_index in p2_contamination:
                     red()
              else:
                     if choice_index == 0:
                            action(random.choice(p2_1))
                     elif choice_index == 1:
                            action(random.choice(p2_2))
                     elif choice_index == 2:
                            action(random.choice(p2_3))
       if current_player_number == 3:
              if choice_index in p3_contamination:
                     red()
              else:
                     if choice_index == 0:
                            action(random.choice(p3_1))
                     elif choice_index == 1:
                            action(random.choice(p3_2))
                     elif choice_index == 2:
                            action(random.choice(p3_3))
       if current_player_number == 4:
              if choice_index in p4_contamination:
                     red()
              else:
                     if choice_index == 0:
                            action(random.choice(p4_1))
                     elif choice_index == 1:
                            action(random.choice(p4_2))
                     elif choice_index == 2:
                            action(random.choice(p4_3))

def abilities():
       pass

def pvp():
       global current_player, current_player_number, p1_stats, p2_stats, p3_stats, p4_stats
       if len(active_players) > 1:
              loopDone = False
              pvp_stats()
              while loopDone == False:
                     combatant = input("Choose a player to engage with: ")
                     try:
                            combatant = int(combatant)
                     except ValueError:
                            print("Invalid input, please enter a number.")
                            continue
                     if current_player_number == combatant:
                            print("You cannot combat yourself, select someone else.")
                     elif combatant not in active_players:
                            print("That player has been eliminated, select someone else.")
                     elif combatant > 0 and combatant < 5:
                            loopDone = True
                            if combatant == 1:
                                   combatant = p1_stats
                            elif combatant == 2:
                                   combatant = p2_stats
                            elif combatant == 3:
                                   combatant = p3_stats
                            elif combatant == 4:
                                   combatant = p4_stats
                            if current_player[STRENGTH_KEY] == 0:
                                   c1_attack = 0
                            else:
                                   c1_attack = random.randint(1, current_player[STRENGTH_KEY])
                            if combatant[STRENGTH_KEY] == 0:
                                   c2_attack = 0
                            else:
                                   c2_attack = random.randint(1, combatant[STRENGTH_KEY])
                            if c1_attack > c2_attack:
                                   damage = c1_attack - c2_attack
                                   print(f"You dealt {damage} damage to your opponent!")
                                   combatant[HEALTH_KEY] -= damage
                            elif c1_attack < c2_attack:
                                   damage = c2_attack - c1_attack
                                   print(f"Your opponent dealt {damage} damage to you!")
                                   current_player[HEALTH_KEY] -= damage
                            elif c1_attack == c2_attack:
                                   print("You and your opponent were equal matches for each other!")
                     else:
                            print("Invalid input, please try again.")
       else:
              print("You are the only player left, there is no one to engage with!")

def pvp_stats():
       global pvp_stats_list
       pvp_stats_list = []
       loopTimes = 1
       p1_min_health = p1_stats[HEALTH_KEY]
       p1_max_health = p1_stats[HEALTH_KEY]
       p1_min_strength = p1_stats[STRENGTH_KEY]
       p1_max_strength = p1_stats[STRENGTH_KEY]
       p2_min_health = p2_stats[HEALTH_KEY]
       p2_max_health = p2_stats[HEALTH_KEY]
       p2_min_strength = p2_stats[STRENGTH_KEY]
       p2_max_strength = p2_stats[STRENGTH_KEY]
       p3_min_health = p3_stats[HEALTH_KEY]
       p3_max_health = p3_stats[HEALTH_KEY]
       p3_min_strength = p3_stats[STRENGTH_KEY]
       p3_max_strength = p3_stats[STRENGTH_KEY]
       p4_min_health = p4_stats[HEALTH_KEY]
       p4_max_health = p4_stats[HEALTH_KEY]
       p4_min_strength = p4_stats[STRENGTH_KEY]
       p4_max_strength = p4_stats[STRENGTH_KEY]
       stats = [p1_min_health, p1_max_health, p1_min_strength, p1_max_strength, p2_min_health, p2_max_health, p2_min_strength, 
                p2_max_strength, p3_min_health, p3_max_health, p3_min_strength, p3_max_strength, p4_min_health, p4_max_health, 
                p4_min_strength, p4_max_strength]
       for stat in stats:
              possibility = random.randint(1, 3)
              while possibility < 3:
                     if loopTimes % 2 == 1:
                            stat -= random.randint(1, 3)
                     elif loopTimes % 2 == 0:
                            stat += random.randint(1, 3)
                     possibility = random.randint(1, 3)
              pvp_stats_list.append(stat)
              loopTimes += 1
       if current_player_number == 1:
              print("Player 1 (You)")
              print (f"Health: {p1_stats[HEALTH_KEY]}")
              print (f"Strength: {p1_stats[STRENGTH_KEY]}")
              print()
              if 2 in active_players:
                     print("Player 2")
                     print (f"Health: {pvp_stats_list[4]} - {pvp_stats_list[5]}")
                     print (f"Strength: {pvp_stats_list[6]} - {pvp_stats_list[7]}")
                     print()
              if 3 in active_players:
                     print("Player 3")
                     print (f"Health: {pvp_stats_list[8]} - {pvp_stats_list[9]}")
                     print (f"Strength: {pvp_stats_list[10]} - {pvp_stats_list[11]}")
                     print()
              if 4 in active_players:
                     print("Player 4")
                     print (f"Health: {pvp_stats_list[12]} - {pvp_stats_list[13]}")
                     print (f"Strength: {pvp_stats_list[14]} - {pvp_stats_list[15]}")
                     print()
       elif current_player_number == 2:
              if 1 in active_players:
                     print("Player 1")
                     print (f"Health: {pvp_stats_list[0]} - {pvp_stats_list[1]}")
                     print (f"Strength: {pvp_stats_list[2]} - {pvp_stats_list[3]}")
                     print()
              print("Player 2 (You)")
              print (f"Health: {p2_stats[HEALTH_KEY]}")
              print (f"Strength: {p2_stats[STRENGTH_KEY]}")
              print()
              if 3 in active_players:
                     print("Player 3")
                     print (f"Health: {pvp_stats_list[8]} - {pvp_stats_list[9]}")
                     print (f"Strength: {pvp_stats_list[10]} - {pvp_stats_list[11]}")
                     print()
              if 4 in active_players:
                     print("Player 4")
                     print (f"Health: {pvp_stats_list[12]} - {pvp_stats_list[13]}")
                     print (f"Strength: {pvp_stats_list[14]} - {pvp_stats_list[15]}")
                     print()
       elif current_player_number == 3:
              if 1 in active_players:
                     print("Player 1")
                     print (f"Health: {pvp_stats_list[0]} - {pvp_stats_list[1]}")
                     print (f"Strength: {pvp_stats_list[2]} - {pvp_stats_list[3]}")
                     print()
              if 2 in active_players:
                     print("Player 2")
              print (f"Health: {pvp_stats_list[4]} - {pvp_stats_list[5]}")
              print (f"Strength: {pvp_stats_list[6]} - {pvp_stats_list[7]}")
              print()
              print("Player 3 (You)")
              print (f"Health: {p3_stats[HEALTH_KEY]}")
              print (f"Strength: {p3_stats[STRENGTH_KEY]}")
              print()
              if 4 in active_players:
                     print("Player 4")
                     print (f"Health: {pvp_stats_list[12]} - {pvp_stats_list[13]}")
                     print (f"Strength: {pvp_stats_list[14]} - {pvp_stats_list[15]}")
                     print()
       elif current_player_number == 4:
              if 1 in active_players:
                     print("Player 1")
                     print (f"Health: {pvp_stats_list[0]} - {pvp_stats_list[1]}")
                     print (f"Strength: {pvp_stats_list[2]} - {pvp_stats_list[3]}")
                     print()
              if 2 in active_players:
                     print("Player 2")
                     print (f"Health: {pvp_stats_list[4]} - {pvp_stats_list[5]}")
                     print (f"Strength: {pvp_stats_list[6]} - {pvp_stats_list[7]}")
                     print()
              if 3 in active_players:
                     print("Player 3")
                     print (f"Health: {pvp_stats_list[8]} - {pvp_stats_list[9]}")
                     print (f"Strength: {pvp_stats_list[10]} - {pvp_stats_list[11]}")
                     print()
              print("Player 4 (You)")
              print (f"Health: {p4_stats[HEALTH_KEY]}")
              print (f"Strength: {p4_stats[STRENGTH_KEY]}")
              print()


def stat_update(happening):
       global current_player, current_player_number, enemy_min, enemy_max, p1_blind, p2_blind, p3_blind, p4_blind

       if happening == RED_OPTIONS[0]:
              LoopDone = False
              while LoopDone == False:
                     if current_player_number == 1:
                            if len(p1_contamination) == 3:
                                   LoopDone = True
                            else:
                                   random_contamination = random.randint(0, 2)
                                   if random_contamination in p1_contamination:
                                          pass
                                   else:
                                          p1_contamination.append(random_contamination)
                                          print(f"You have been contaminated in square {random_contamination + 1}!")
                                          LoopDone = True
                     elif current_player_number == 2:
                            if len(p2_contamination) == 3:
                                   LoopDone = True
                            else:
                                   random_contamination = random.randint(0, 2)
                                   if random_contamination in p2_contamination:
                                          pass
                                   else:
                                          p2_contamination.append(random_contamination)
                                          print(f"You have been contaminated in square {random_contamination + 1}!")
                                          LoopDone = True
                     elif current_player_number == 3:
                            if len(p3_contamination) == 3:
                                   LoopDone = True
                            else:
                                   random_contamination = random.randint(0, 2)
                                   if random_contamination in p3_contamination:
                                          pass
                                   else:
                                          p3_contamination.append(random_contamination)
                                          print(f"You have been contaminated in square {random_contamination + 1}!")
                                          LoopDone = True
                     elif current_player_number == 4:
                            if len(p4_contamination) == 3:
                                   LoopDone = True
                            else:
                                   random_contamination = random.randint(0, 2)
                                   if random_contamination in p4_contamination:
                                          pass
                                   else:
                                          p4_contamination.append(random_contamination)
                                          print(f"You have been contaminated in square {random_contamination + 1}!")
                                          LoopDone = True
       elif happening == RED_OPTIONS[1]:
              current_player[GOLD_KEY] -= 1
       elif happening == RED_OPTIONS[2]:
              if current_player[POINTS_KEY] > 0:
                     current_player[POINTS_KEY] -= 1
       elif happening == RED_OPTIONS[3]:
              if current_player[STRENGTH_KEY] > 0:
                     current_player[STRENGTH_KEY] -= 1
       elif happening == RED_OPTIONS[4]:
              current_player[HEALTH_KEY] -= 1
       elif happening == RED_OPTIONS[5]:
              current_player[GOLD_KEY] -= 3
       elif happening == RED_OPTIONS[6]:
              if current_player[STRENGTH_KEY] > 2:
                     current_player[STRENGTH_KEY] -= 3
              else:
                     current_player[STRENGTH_KEY] = 0
       elif happening == RED_OPTIONS[7]:
              current_player[HEALTH_KEY] -= 3
       elif happening == RED_OPTIONS[8]:
              if current_player_number == 1:
                     p1_blind = True
              elif current_player_number == 2:
                     p2_blind = True
              elif current_player_number == 3:
                     p3_blind = True
              elif current_player_number == 4:
                     p4_blind = True
       elif happening == RED_OPTIONS[10]:
              if enemy_min == 1:
                     enemy_min = 5
              else:
                     enemy_min += 5
              if enemy_min > enemy_max:
                     enemy_max = enemy_min 
       elif happening == RED_OPTIONS[11]:
                     if enemy_max == 1:
                            enemy_max = 5
                     else:
                            enemy_max += 5
       elif happening == RED_OPTIONS[12]:
              orange()
       elif happening == RED_OPTIONS[13]:
              purple()
       elif happening == RED_OPTIONS[14]:
              red()
              red()
       elif happening == RED_OPTIONS[15]:
              current_player[HEALTH_KEY] -= 1
              if current_player[STRENGTH_KEY] > 0:
                     current_player[STRENGTH_KEY] -= 1
              current_player[GOLD_KEY] -= 1
              if current_player[POINTS_KEY] > 0:
                     current_player[POINTS_KEY] -= 1


       elif happening == ORANGE_OPTIONS[0]:
              current_player[GOLD_KEY] += 1
       elif happening == ORANGE_OPTIONS[1]:
              if current_player[POINTS_KEY] == 10:
                     print("You have already reached max points!")
              elif current_player[GOLD_KEY] < 0:
                     print("You have negative gold, have a bad fortune instead!")
                     red()
              else:
                     print("You have gained 1 point!")
                     current_player[POINTS_KEY] += 1
       elif happening == ORANGE_OPTIONS[2]:
              current_player[STRENGTH_KEY] += 1
       elif happening == ORANGE_OPTIONS[3]:
              current_player[HEALTH_KEY] += 1
       elif happening == ORANGE_OPTIONS[4]:
              current_player[GOLD_KEY] += 3
       elif happening == ORANGE_OPTIONS[5]:
              current_player[STRENGTH_KEY] += 3
       elif happening == ORANGE_OPTIONS[6]:
              current_player[HEALTH_KEY] += 3
       elif happening == ORANGE_OPTIONS[7]:
              if current_player_number == 1:
                     if p1_blind == True:
                            p1_blind = False
                            print("You are no longer blind!")
                     elif mode == "S":
                            if p2_blind == True:
                                   p2_blind = False
                                   print("Player 2 is no longer blind!")
                            elif p3_blind == True:
                                   p3_blind = False
                                   print("Player 3 is no longer blind!")
                            elif p4_blind == True:
                                   p4_blind = False
                                   print("Player 4 is no longer blind!")
                            else:
                                   print("No one is blind")
                     else:
                            print("You're not blind")
              elif current_player_number == 2:
                     if p2_blind == True:
                            p2_blind = False
                            print("You are no longer blind!")
                     elif mode == "S":
                            if p3_blind == True:
                                   p3_blind = False
                                   print("Player 3 is no longer blind!")
                            elif p4_blind == True:
                                   p4_blind = False
                                   print("Player 4 is no longer blind!")
                            elif p1_blind == True:
                                   p1_blind = False
                                   print("Player 1 is no longer blind!")
                            else:
                                   print("No one is blind!")
                     else:
                            print("You're not blind")
              elif current_player_number == 3:
                     if p3_blind == True:
                            p3_blind = False
                            print("You are no longer blind!")
                     elif mode == "S":
                            if p4_blind == True:
                                   p4_blind = False
                                   print("Player 4 is no longer blind!")
                            elif p1_blind == True:
                                   p1_blind = False
                                   print("Player 1 is no longer blind!")
                            elif p2_blind == True:
                                   p2_blind = False
                                   print("Player 2 is no longer blind!")
                            else:
                                   print("No one is blind!")
                     else:
                            print("You're not blind")
              elif current_player_number == 4:
                     if p4_blind == True:
                            p4_blind = False
                            print("You are no longer blind!")
                     elif mode == "S":
                            if p1_blind == True:
                                   p1_blind = False
                                   print("Player 1 is no longer blind!")
                            elif p2_blind == True:
                                   p2_blind = False
                                   print("Player 2 is no longer blind!")
                            elif p3_blind == True:
                                   p3_blind = False
                                   print("Player 3 is no longer blind!")
                            else:
                                   print("No one is blind!")
                     else:
                            print("You're not blind")
       elif happening == ORANGE_OPTIONS[9]:
              if current_player_number == 1:
                     if len(p1_contamination) > 0:
                            random_cure = random.randrange(len(p1_contamination))
                            p1_contamination.pop(random_cure)
                            print(f"You have been cured of contamination in square {random_cure + 1}!")
                     elif mode == "S":
                            if len(p2_contamination) > 0:
                                   random_cure = random.randrange(len(p2_contamination))
                                   p2_contamination.pop(random_cure)
                                   print(f"Player 2 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p3_contamination) > 0:
                                   random_cure = random.randrange(len(p3_contamination))
                                   p3_contamination.pop(random_cure)
                                   print(f"Player 3 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p4_contamination) > 0:
                                   random_cure = random.randrange(len(p4_contamination))
                                   p4_contamination.pop(random_cure)
                                   print(f"Player 4 has been cured of contamination in square {random_cure + 1}!")
                            else:
                                   print("No one is contaminated")
                     else:
                            print("You're not contaminated")
              elif current_player_number == 2:
                     if len(p2_contamination) > 0:
                            random_cure = random.randrange(len(p2_contamination))
                            p2_contamination.pop(random_cure)
                            print(f"You have been cured of contamination in square {random_cure + 1}!")
                     elif mode == "S":
                            if len(p3_contamination) > 0:
                                   random_cure = random.randrange(len(p3_contamination))
                                   p3_contamination.pop(random_cure)
                                   print(f"Player 3 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p4_contamination) > 0:
                                   random_cure = random.randrange(len(p4_contamination))
                                   p4_contamination.pop(random_cure)
                                   print(f"Player 4 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p1_contamination) > 0:
                                   random_cure = random.randrange(len(p1_contamination))
                                   p1_contamination.pop(random_cure)
                                   print(f"Player 1 has been cured of contamination in square {random_cure + 1}!")
                            else:
                                   print("No one is contaminated")
                     else:
                            print("You're not contaminated")
              elif current_player_number == 3:
                     if len(p3_contamination) > 0:
                            random_cure = random.randrange(len(p3_contamination))
                            p3_contamination.pop(random_cure)
                            print(f"You have been cured of contamination in square {random_cure + 1}!")
                     elif mode == "S":
                            if len(p4_contamination) > 0:
                                   random_cure = random.randrange(len(p4_contamination))
                                   p4_contamination.pop(random_cure)
                                   print(f"Player 4 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p1_contamination) > 0:
                                   random_cure = random.randrange(len(p1_contamination))
                                   p1_contamination.pop(random_cure)
                                   print(f"Player 1 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p2_contamination) > 0:
                                   random_cure = random.randrange(len(p2_contamination))
                                   p2_contamination.pop(random_cure)
                                   print(f"Player 2 has been cured of contamination in square {random_cure + 1}!")
                            else:
                                   print("No one is contaminated")
                     else:
                            print("You're not contaminated")
              if current_player_number == 4:
                     if len(p4_contamination) > 0:
                            random_cure = random.randrange(len(p4_contamination))
                            p4_contamination.pop(random_cure)
                            print(f"You have been cured of contamination in square {random_cure + 1}!")
                     elif mode == "S":
                            if len(p1_contamination) > 0:
                                   random_cure = random.randrange(len(p1_contamination))
                                   p1_contamination.pop(random_cure)
                                   print(f"Player 1 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p2_contamination) > 0:
                                   random_cure = random.randrange(len(p2_contamination))
                                   p2_contamination.pop(random_cure)
                                   print(f"Player 2 has been cured of contamination in square {random_cure + 1}!")
                            elif len(p3_contamination) > 0:
                                   random_cure = random.randrange(len(p3_contamination))
                                   p3_contamination.pop(random_cure)
                                   print(f"Player 3 has been cured of contamination in square {random_cure + 1}!")
                            else:
                                   print("No one is contaminated")
                     else:
                            print("You're not contaminated")
       elif happening == ORANGE_OPTIONS[10]:
              red()
       elif happening == ORANGE_OPTIONS[12]:
              orange()
              orange()
       elif happening == ORANGE_OPTIONS[13]:
              current_player[HEALTH_KEY] += 1
              current_player[STRENGTH_KEY] += 1
              current_player[GOLD_KEY] += 1
              if current_player[POINTS_KEY] < 10:
                     current_player[POINTS_KEY] += 1
       # elif happening == ORANGE_OPTIONS[14]:
       #        abilities()


       elif happening == PURPLE_OPTIONS[0]:
              if enemy_max == 5:
                     enemy_max = 1
              elif enemy_max == 1:
                     pass
              else:
                     enemy_max -= 5
              if enemy_min > enemy_max:
                     enemy_min = enemy_max
       elif happening == PURPLE_OPTIONS[1]:
              if enemy_min == 5:
                     enemy_min = 1
              elif enemy_min == 1:
                     pass
              else:
                     enemy_min -= 5
       elif happening == PURPLE_OPTIONS[10]:
              enemy_min = enemy_max
       elif happening == PURPLE_OPTIONS[11]:
              enemy_max = enemy_min
       elif happening == PURPLE_OPTIONS[21]:
              chance()
       elif happening == PURPLE_OPTIONS[22]:
              square_change()
       elif happening == PURPLE_OPTIONS[23]:
              purple()
              purple()
        
def encounter():
       global current_player, current_player_number, enemy_min, enemy_max, p1_stats, p2_stats, p3_stats, p4_stats
       enemy_strength = random.randint(enemy_min, enemy_max)
       enemy_attack = random.randint(1, enemy_strength)
       player_strength = current_player[STRENGTH_KEY]
       if player_strength > 0:
              player_attack = random.randint(1, player_strength)
       else:
              player_attack = 0
       print(f"An enemy appears!")
       if player_attack > enemy_attack:
              print(f"You defeated the enemy!")
              orange()
       elif player_attack < enemy_attack:
              damage = enemy_attack - player_attack
              current_player[HEALTH_KEY] -= damage
              print(f"You were hit for {damage} damage!")
              red()
       else:
              print(f"You and the enemy are equally strong, and it is a tie")
              brown()
       
def action(choice):
       if choice == "🟥":
              happening = red()
              return happening
       elif choice == "🟧":
              happening = orange()
              return happening
       elif choice == "🟪":
              happening = purple()
              return happening
       elif choice == "🟨":
              happening = shop()
              return happening
       elif choice == "🟩":
              happening = green()
              return happening
       elif choice == "🟫":
              happening = brown()
              return happening
       elif choice == "⬛":
              happening = black()
              return happening
       elif choice == "⬜":
              happening = square_change()
              return happening
       elif choice == "🟦":
              happening = chance()
              return happening
       elif choice == "➖":
              happening = blind()
              return happening
       elif choice == "⚔️ ":
              happening = pvp()
              return happening
       else:
              print("You messed up")
       
def stats():
       print()
       print("Player 1:")
       print(f"Health: {p1_stats[HEALTH_KEY]}")
       print(f"Strength: {p1_stats[STRENGTH_KEY]}")
       print(f"Gold: {p1_stats[GOLD_KEY]}")
       print(f"Points: {p1_stats[POINTS_KEY]}")
       print(f"Contamination:")
       for i in p1_contamination:
              print(f"  - Square {i + 1}")
       print()
       print("Player 2:")
       print(f"Health: {p2_stats[HEALTH_KEY]}")
       print(f"Strength: {p2_stats[STRENGTH_KEY]}")
       print(f"Gold: {p2_stats[GOLD_KEY]}")
       print(f"Points: {p2_stats[POINTS_KEY]}")
       print(f"Contamination:")
       for i in p2_contamination:
              print(f"  - Square {i + 1}")
       print()
       print("Player 3:")
       print(f"Health: {p3_stats[HEALTH_KEY]}")
       print(f"Strength: {p3_stats[STRENGTH_KEY]}")
       print(f"Gold: {p3_stats[GOLD_KEY]}")
       print(f"Points: {p3_stats[POINTS_KEY]}")
       print(f"Contamination:")
       for i in p3_contamination:
              print(f"  - Square {i + 1}")
       print()
       print("Player 4:")
       print(f"Health: {p4_stats[HEALTH_KEY]}")
       print(f"Strength: {p4_stats[STRENGTH_KEY]}")
       print(f"Gold: {p4_stats[GOLD_KEY]}")
       print(f"Points: {p4_stats[POINTS_KEY]}")
       print(f"Contamination:")
       for i in p4_contamination:
              print(f"  - Square {i + 1}")
       print()
       print("Enemies:")
       print(f"Average Strength: {(enemy_max + enemy_min) / 2}")
       print(f"Minimum Strength: {enemy_min}")
       print(f"Maximum Strength: {enemy_max}")

def multi_stats(player):
       if player == 0:
              print()
              print("Player 1:")
              print(f"Health: {p1_stats[HEALTH_KEY]}")
              print(f"Strength: {p1_stats[STRENGTH_KEY]}")
              print(f"Gold: {p1_stats[GOLD_KEY]}")
              print(f"Points: {p1_stats[POINTS_KEY]}")
              print(f"Contamination:")
              for i in p1_contamination:
                     print(f"  - Square {i + 1}")
       elif player == 1:
              print()
              print("Player 2:")
              print(f"Health: {p2_stats[HEALTH_KEY]}")
              print(f"Strength: {p2_stats[STRENGTH_KEY]}")
              print(f"Gold: {p2_stats[GOLD_KEY]}")
              print(f"Points: {p2_stats[POINTS_KEY]}")
              print(f"Contamination:")
              for i in p2_contamination:
                     print(f"  - Square {i + 1}")
       elif player == 2:
              print()
              print("Player 3:")
              print(f"Health: {p3_stats[HEALTH_KEY]}")
              print(f"Strength: {p3_stats[STRENGTH_KEY]}")
              print(f"Gold: {p3_stats[GOLD_KEY]}")
              print(f"Points: {p3_stats[POINTS_KEY]}")
              print(f"Contamination:")
              for i in p3_contamination:
                     print(f"  - Square {i + 1}")
       elif player == 3:
              print()
              print("Player 4:")
              print(f"Health: {p4_stats[HEALTH_KEY]}")
              print(f"Strength: {p4_stats[STRENGTH_KEY]}")
              print(f"Gold: {p4_stats[GOLD_KEY]}")
              print(f"Points: {p4_stats[POINTS_KEY]}")
              print(f"Contamination:")
              for i in p4_contamination:
                     print(f"  - Square {i + 1}")
       print()
       print("Enemies:")
       print(f"Average Strength: {(enemy_max + enemy_min) / 2}")
       print(f"Minimum Strength: {enemy_min}")
       print(f"Maximum Strength: {enemy_max}")

#🟨, 🟪, 🟧, 🟥, 🟩, 🟫, ⬛, 🟦, ⬜, ➖

def square_list():
       validChoice = False
       while validChoice == False:
              player = input("Which player's squares would you like to view?: ")
              if player == "1":
                     print("Player 1:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p1_1.count("🟨") / len(p1_1) * 100, 1)}%")
                     print(f"Purple: {round(p1_1.count("🟪") / len(p1_1) * 100, 1)}%")
                     print(f"Orange: {round(p1_1.count("🟧") / len(p1_1) * 100, 1)}%")
                     print(f"Red: {round(p1_1.count("🟥") / len(p1_1) * 100, 1)}%")
                     print(f"Green: {round(p1_1.count("🟩") / len(p1_1) * 100, 1)}%")
                     print(f"Brown: {round(p1_1.count("🟫") / len(p1_1) * 100, 1)}%")
                     print(f"Black: {round(p1_1.count("⬛") / len(p1_1) * 100, 1)}%")
                     print(f"Blue: {round(p1_1.count("🟦") / len(p1_1) * 100, 1)}%")
                     print(f"White: {round(p1_1.count("⬜") / len(p1_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p1_2.count("🟨") / len(p1_2) * 100, 1)}%")
                     print(f"Purple: {round(p1_2.count("🟪") / len(p1_2) * 100, 1)}%")
                     print(f"Orange: {round(p1_2.count("🟧") / len(p1_2) * 100, 1)}%")
                     print(f"Red: {round(p1_2.count("🟥") / len(p1_2) * 100, 1)}%")
                     print(f"Green: {round(p1_2.count("🟩") / len(p1_2) * 100, 1)}%")
                     print(f"Brown: {round(p1_2.count("🟫") / len(p1_2) * 100, 1)}%")
                     print(f"Black: {round(p1_2.count("⬛") / len(p1_2) * 100, 1)}%")
                     print(f"Blue: {round(p1_2.count("🟦") / len(p1_2) * 100, 1)}%")
                     print(f"White: {round(p1_2.count("⬜") / len(p1_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p1_3.count("🟨") / len(p1_3) * 100, 1)}%")
                     print(f"Purple: {round(p1_3.count("🟪") / len(p1_3) * 100, 1)}%")
                     print(f"Orange: {round(p1_3.count("🟧") / len(p1_3) * 100, 1)}%")
                     print(f"Red: {round(p1_3.count("🟥") / len(p1_3) * 100, 1)}%")
                     print(f"Green: {round(p1_3.count("🟩") / len(p1_3) * 100, 1)}%")
                     print(f"Brown: {round(p1_3.count("🟫") / len(p1_3) * 100, 1)}%")
                     print(f"Black: {round(p1_3.count("⬛") / len(p1_3) * 100, 1)}%")
                     print(f"Blue: {round(p1_3.count("🟦") / len(p1_3) * 100, 1)}%")
                     print(f"White: {round(p1_3.count("⬜") / len(p1_3) * 100, 1)}%")
                     print()
                     validChoice = True
              elif player == "2":
                     print("Player 2:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p2_1.count("🟨") / len(p2_1) * 100, 1)}%")
                     print(f"Purple: {round(p2_1.count("🟪") / len(p2_1) * 100, 1)}%")
                     print(f"Orange: {round(p2_1.count("🟧") / len(p2_1) * 100, 1)}%")
                     print(f"Red: {round(p2_1.count("🟥") / len(p2_1) * 100, 1)}%")
                     print(f"Green: {round(p2_1.count("🟩") / len(p2_1) * 100, 1)}%")
                     print(f"Brown: {round(p2_1.count("🟫") / len(p2_1) * 100, 1)}%")
                     print(f"Black: {round(p2_1.count("⬛") / len(p2_1) * 100, 1)}%")
                     print(f"Blue: {round(p2_1.count("🟦") / len(p2_1) * 100, 1)}%")
                     print(f"White: {round(p2_1.count("⬜") / len(p2_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p2_2.count("🟨") / len(p2_2) * 100, 1)}%")
                     print(f"Purple: {round(p2_2.count("🟪") / len(p2_2) * 100, 1)}%")
                     print(f"Orange: {round(p2_2.count("🟧") / len(p2_2) * 100, 1)}%")
                     print(f"Red: {round(p2_2.count("🟥") / len(p2_2) * 100, 1)}%")
                     print(f"Green: {round(p2_2.count("🟩") / len(p2_2) * 100, 1)}%")
                     print(f"Brown: {round(p2_2.count("🟫") / len(p2_2) * 100, 1)}%")
                     print(f"Black: {round(p2_2.count("⬛") / len(p2_2) * 100, 1)}%")
                     print(f"Blue: {round(p2_2.count("🟦") / len(p2_2) * 100, 1)}%")
                     print(f"White: {round(p2_2.count("⬜") / len(p2_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p2_3.count("🟨") / len(p2_3) * 100, 1)}%")
                     print(f"Purple: {round(p2_3.count("🟪") / len(p2_3) * 100, 1)}%")
                     print(f"Orange: {round(p2_3.count("🟧") / len(p2_3) * 100, 1)}%")
                     print(f"Red: {round(p2_3.count("🟥") / len(p2_3) * 100, 1)}%")
                     print(f"Green: {round(p2_3.count("🟩") / len(p2_3) * 100, 1)}%")
                     print(f"Brown: {round(p2_3.count("🟫") / len(p2_3) * 100, 1)}%")
                     print(f"Black: {round(p2_3.count("⬛") / len(p2_3) * 100, 1)}%")
                     print(f"Blue: {round(p2_3.count("🟦") / len(p2_3) * 100, 1)}%")
                     print(f"White: {round(p2_3.count("⬜") / len(p2_3) * 100, 1)}%")
                     print()
                     validChoice = True
              elif player == "3":
                     print("Player 3:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p3_1.count("🟨") / len(p3_1) * 100, 1)}%")
                     print(f"Purple: {round(p3_1.count("🟪") / len(p3_1) * 100, 1)}%")
                     print(f"Orange: {round(p3_1.count("🟧") / len(p3_1) * 100, 1)}%")
                     print(f"Red: {round(p3_1.count("🟥") / len(p3_1) * 100, 1)}%")
                     print(f"Green: {round(p3_1.count("🟩") / len(p3_1) * 100, 1)}%")
                     print(f"Brown: {round(p3_1.count("🟫") / len(p3_1) * 100, 1)}%")
                     print(f"Black: {round(p3_1.count("⬛") / len(p3_1) * 100, 1)}%")
                     print(f"Blue: {round(p3_1.count("🟦") / len(p3_1) * 100, 1)}%")
                     print(f"White: {round(p3_1.count("⬜") / len(p3_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p3_2.count("🟨") / len(p3_2) * 100, 1)}%")
                     print(f"Purple: {round(p3_2.count("🟪") / len(p3_2) * 100, 1)}%")
                     print(f"Orange: {round(p3_2.count("🟧") / len(p3_2) * 100, 1)}%")
                     print(f"Red: {round(p3_2.count("🟥") / len(p3_2) * 100, 1)}%")
                     print(f"Green: {round(p3_2.count("🟩") / len(p3_2) * 100, 1)}%")
                     print(f"Brown: {round(p3_2.count("🟫") / len(p3_2) * 100, 1)}%")
                     print(f"Black: {round(p3_2.count("⬛") / len(p3_2) * 100, 1)}%")
                     print(f"Blue: {round(p3_2.count("🟦") / len(p3_2) * 100, 1)}%")
                     print(f"White: {round(p3_2.count("⬜") / len(p3_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p3_3.count("🟨") / len(p3_3) * 100, 1)}%")
                     print(f"Purple: {round(p3_3.count("🟪") / len(p3_3) * 100, 1)}%")
                     print(f"Orange: {round(p3_3.count("🟧") / len(p3_3) * 100, 1)}%")
                     print(f"Red: {round(p3_3.count("🟥") / len(p3_3) * 100, 1)}%")
                     print(f"Green: {round(p3_3.count("🟩") / len(p3_3) * 100, 1)}%")
                     print(f"Brown: {round(p3_3.count("🟫") / len(p3_3) * 100, 1)}%")
                     print(f"Black: {round(p3_3.count("⬛") / len(p3_3) * 100, 1)}%")
                     print(f"Blue: {round(p3_3.count("🟦") / len(p3_3) * 100, 1)}%")
                     print(f"White: {round(p3_3.count("⬜") / len(p3_3) * 100, 1)}%")
                     print()
                     validChoice = True
              elif player == "4":
                     print("Player 4:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p4_1.count("🟨") / len(p4_1) * 100, 1)}%")
                     print(f"Purple: {round(p4_1.count("🟪") / len(p4_1) * 100, 1)}%")
                     print(f"Orange: {round(p4_1.count("🟧") / len(p4_1) * 100, 1)}%")
                     print(f"Red: {round(p4_1.count("🟥") / len(p4_1) * 100, 1)}%")
                     print(f"Green: {round(p4_1.count("🟩") / len(p4_1) * 100, 1)}%")
                     print(f"Brown: {round(p4_1.count("🟫") / len(p4_1) * 100, 1)}%")
                     print(f"Black: {round(p4_1.count("⬛") / len(p4_1) * 100, 1)}%")
                     print(f"Blue: {round(p4_1.count("🟦") / len(p4_1) * 100, 1)}%")
                     print(f"White: {round(p4_1.count("⬜") / len(p4_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p4_2.count("🟨") / len(p4_2) * 100, 1)}%")
                     print(f"Purple: {round(p4_2.count("🟪") / len(p4_2) * 100, 1)}%")
                     print(f"Orange: {round(p4_2.count("🟧") / len(p4_2) * 100, 1)}%")
                     print(f"Red: {round(p4_2.count("🟥") / len(p4_2) * 100, 1)}%")
                     print(f"Green: {round(p4_2.count("🟩") / len(p4_2) * 100, 1)}%")
                     print(f"Brown: {round(p4_2.count("🟫") / len(p4_2) * 100, 1)}%")
                     print(f"Black: {round(p4_2.count("⬛") / len(p4_2) * 100, 1)}%")
                     print(f"Blue: {round(p4_2.count("🟦") / len(p4_2) * 100, 1)}%")
                     print(f"White: {round(p4_2.count("⬜") / len(p4_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p4_3.count("🟨") / len(p4_3) * 100, 1)}%")
                     print(f"Purple: {round(p4_3.count("🟪") / len(p4_3) * 100, 1)}%")
                     print(f"Orange: {round(p4_3.count("🟧") / len(p4_3) * 100, 1)}%")
                     print(f"Red: {round(p4_3.count("🟥") / len(p4_3) * 100, 1)}%")
                     print(f"Green: {round(p4_3.count("🟩") / len(p4_3) * 100, 1)}%")
                     print(f"Brown: {round(p4_3.count("🟫") / len(p4_3) * 100, 1)}%")
                     print(f"Black: {round(p4_3.count("⬛") / len(p4_3) * 100, 1)}%")
                     print(f"Blue: {round(p4_3.count("🟦") / len(p4_3) * 100, 1)}%")
                     print(f"White: {round(p4_3.count("⬜") / len(p4_3) * 100, 1)}%")
                     print()
                     validChoice = True
              else:
                     print("Invalid choice. Please try again.")

def multi_square_list(player):
              if player == 0:
                     print("Player 1:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p1_1.count("🟨") / len(p1_1) * 100, 1)}%")
                     print(f"Purple: {round(p1_1.count("🟪") / len(p1_1) * 100, 1)}%")
                     print(f"Orange: {round(p1_1.count("🟧") / len(p1_1) * 100, 1)}%")
                     print(f"Red: {round(p1_1.count("🟥") / len(p1_1) * 100, 1)}%")
                     print(f"Green: {round(p1_1.count("🟩") / len(p1_1) * 100, 1)}%")
                     print(f"Brown: {round(p1_1.count("🟫") / len(p1_1) * 100, 1)}%")
                     print(f"Black: {round(p1_1.count("⬛") / len(p1_1) * 100, 1)}%")
                     print(f"Blue: {round(p1_1.count("🟦") / len(p1_1) * 100, 1)}%")
                     print(f"White: {round(p1_1.count("⬜") / len(p1_1) * 100, 1)}%")
                     print(f"Sword: {round(p1_1.count("⚔️ ") / len(p1_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p1_2.count("🟨") / len(p1_2) * 100, 1)}%")
                     print(f"Purple: {round(p1_2.count("🟪") / len(p1_2) * 100, 1)}%")
                     print(f"Orange: {round(p1_2.count("🟧") / len(p1_2) * 100, 1)}%")
                     print(f"Red: {round(p1_2.count("🟥") / len(p1_2) * 100, 1)}%")
                     print(f"Green: {round(p1_2.count("🟩") / len(p1_2) * 100, 1)}%")
                     print(f"Brown: {round(p1_2.count("🟫") / len(p1_2) * 100, 1)}%")
                     print(f"Black: {round(p1_2.count("⬛") / len(p1_2) * 100, 1)}%")
                     print(f"Blue: {round(p1_2.count("🟦") / len(p1_2) * 100, 1)}%")
                     print(f"White: {round(p1_2.count("⬜") / len(p1_2) * 100, 1)}%")
                     print(f"Sword: {round(p1_2.count("⚔️ ") / len(p1_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p1_3.count("🟨") / len(p1_3) * 100, 1)}%")
                     print(f"Purple: {round(p1_3.count("🟪") / len(p1_3) * 100, 1)}%")
                     print(f"Orange: {round(p1_3.count("🟧") / len(p1_3) * 100, 1)}%")
                     print(f"Red: {round(p1_3.count("🟥") / len(p1_3) * 100, 1)}%")
                     print(f"Green: {round(p1_3.count("🟩") / len(p1_3) * 100, 1)}%")
                     print(f"Brown: {round(p1_3.count("🟫") / len(p1_3) * 100, 1)}%")
                     print(f"Black: {round(p1_3.count("⬛") / len(p1_3) * 100, 1)}%")
                     print(f"Blue: {round(p1_3.count("🟦") / len(p1_3) * 100, 1)}%")
                     print(f"White: {round(p1_3.count("⬜") / len(p1_3) * 100, 1)}%")
                     print(f"Sword: {round(p1_3.count("⚔️ ") / len(p1_3) * 100, 1)}%")
              elif player == 1:
                     print("Player 2:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p2_1.count("🟨") / len(p2_1) * 100, 1)}%")
                     print(f"Purple: {round(p2_1.count("🟪") / len(p2_1) * 100, 1)}%")
                     print(f"Orange: {round(p2_1.count("🟧") / len(p2_1) * 100, 1)}%")
                     print(f"Red: {round(p2_1.count("🟥") / len(p2_1) * 100, 1)}%")
                     print(f"Green: {round(p2_1.count("🟩") / len(p2_1) * 100, 1)}%")
                     print(f"Brown: {round(p2_1.count("🟫") / len(p2_1) * 100, 1)}%")
                     print(f"Black: {round(p2_1.count("⬛") / len(p2_1) * 100, 1)}%")
                     print(f"Blue: {round(p2_1.count("🟦") / len(p2_1) * 100, 1)}%")
                     print(f"White: {round(p2_1.count("⬜") / len(p2_1) * 100, 1)}%")
                     print(f"Sword: {round(p2_1.count("⚔️ ") / len(p2_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p2_2.count("🟨") / len(p2_2) * 100, 1)}%")
                     print(f"Purple: {round(p2_2.count("🟪") / len(p2_2) * 100, 1)}%")
                     print(f"Orange: {round(p2_2.count("🟧") / len(p2_2) * 100, 1)}%")
                     print(f"Red: {round(p2_2.count("🟥") / len(p2_2) * 100, 1)}%")
                     print(f"Green: {round(p2_2.count("🟩") / len(p2_2) * 100, 1)}%")
                     print(f"Brown: {round(p2_2.count("🟫") / len(p2_2) * 100, 1)}%")
                     print(f"Black: {round(p2_2.count("⬛") / len(p2_2) * 100, 1)}%")
                     print(f"Blue: {round(p2_2.count("🟦") / len(p2_2) * 100, 1)}%")
                     print(f"White: {round(p2_2.count("⬜") / len(p2_2) * 100, 1)}%")
                     print(f"Sword: {round(p2_2.count("⚔️ ") / len(p2_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p2_3.count("🟨") / len(p2_3) * 100, 1)}%")
                     print(f"Purple: {round(p2_3.count("🟪") / len(p2_3) * 100, 1)}%")
                     print(f"Orange: {round(p2_3.count("🟧") / len(p2_3) * 100, 1)}%")
                     print(f"Red: {round(p2_3.count("🟥") / len(p2_3) * 100, 1)}%")
                     print(f"Green: {round(p2_3.count("🟩") / len(p2_3) * 100, 1)}%")
                     print(f"Brown: {round(p2_3.count("🟫") / len(p2_3) * 100, 1)}%")
                     print(f"Black: {round(p2_3.count("⬛") / len(p2_3) * 100, 1)}%")
                     print(f"Blue: {round(p2_3.count("🟦") / len(p2_3) * 100, 1)}%")
                     print(f"White: {round(p2_3.count("⬜") / len(p2_3) * 100, 1)}%")
                     print(f"Sword: {round(p2_3.count("⚔️ ") / len(p2_3) * 100, 1)}%")
                     print()
              elif player == 2:
                     print("Player 3:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p3_1.count("🟨") / len(p3_1) * 100, 1)}%")
                     print(f"Purple: {round(p3_1.count("🟪") / len(p3_1) * 100, 1)}%")
                     print(f"Orange: {round(p3_1.count("🟧") / len(p3_1) * 100, 1)}%")
                     print(f"Red: {round(p3_1.count("🟥") / len(p3_1) * 100, 1)}%")
                     print(f"Green: {round(p3_1.count("🟩") / len(p3_1) * 100, 1)}%")
                     print(f"Brown: {round(p3_1.count("🟫") / len(p3_1) * 100, 1)}%")
                     print(f"Black: {round(p3_1.count("⬛") / len(p3_1) * 100, 1)}%")
                     print(f"Blue: {round(p3_1.count("🟦") / len(p3_1) * 100, 1)}%")
                     print(f"White: {round(p3_1.count("⬜") / len(p3_1) * 100, 1)}%")
                     print(f"Sword: {round(p3_1.count("⚔️ ") / len(p3_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p3_2.count("🟨") / len(p3_2) * 100, 1)}%")
                     print(f"Purple: {round(p3_2.count("🟪") / len(p3_2) * 100, 1)}%")
                     print(f"Orange: {round(p3_2.count("🟧") / len(p3_2) * 100, 1)}%")
                     print(f"Red: {round(p3_2.count("🟥") / len(p3_2) * 100, 1)}%")
                     print(f"Green: {round(p3_2.count("🟩") / len(p3_2) * 100, 1)}%")
                     print(f"Brown: {round(p3_2.count("🟫") / len(p3_2) * 100, 1)}%")
                     print(f"Black: {round(p3_2.count("⬛") / len(p3_2) * 100, 1)}%")
                     print(f"Blue: {round(p3_2.count("🟦") / len(p3_2) * 100, 1)}%")
                     print(f"White: {round(p3_2.count("⬜") / len(p3_2) * 100, 1)}%")
                     print(f"Sword: {round(p3_2.count("⚔️ ") / len(p3_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p3_3.count("🟨") / len(p3_3) * 100, 1)}%")
                     print(f"Purple: {round(p3_3.count("🟪") / len(p3_3) * 100, 1)}%")
                     print(f"Orange: {round(p3_3.count("🟧") / len(p3_3) * 100, 1)}%")
                     print(f"Red: {round(p3_3.count("🟥") / len(p3_3) * 100, 1)}%")
                     print(f"Green: {round(p3_3.count("🟩") / len(p3_3) * 100, 1)}%")
                     print(f"Brown: {round(p3_3.count("🟫") / len(p3_3) * 100, 1)}%")
                     print(f"Black: {round(p3_3.count("⬛") / len(p3_3) * 100, 1)}%")
                     print(f"Blue: {round(p3_3.count("🟦") / len(p3_3) * 100, 1)}%")
                     print(f"White: {round(p3_3.count("⬜") / len(p3_3) * 100, 1)}%")
                     print(f"Sword: {round(p3_3.count("⚔️ ") / len(p3_3) * 100, 1)}%")
                     print()
              elif player == 3:
                     print("Player 4:")
                     print()
                     print("Position 1:")
                     print(f"Yellow: {round(p4_1.count("🟨") / len(p4_1) * 100, 1)}%")
                     print(f"Purple: {round(p4_1.count("🟪") / len(p4_1) * 100, 1)}%")
                     print(f"Orange: {round(p4_1.count("🟧") / len(p4_1) * 100, 1)}%")
                     print(f"Red: {round(p4_1.count("🟥") / len(p4_1) * 100, 1)}%")
                     print(f"Green: {round(p4_1.count("🟩") / len(p4_1) * 100, 1)}%")
                     print(f"Brown: {round(p4_1.count("🟫") / len(p4_1) * 100, 1)}%")
                     print(f"Black: {round(p4_1.count("⬛") / len(p4_1) * 100, 1)}%")
                     print(f"Blue: {round(p4_1.count("🟦") / len(p4_1) * 100, 1)}%")
                     print(f"White: {round(p4_1.count("⬜") / len(p4_1) * 100, 1)}%")
                     print(f"Sword: {round(p4_1.count("⚔️ ") / len(p4_1) * 100, 1)}%")
                     print()
                     print("Position 2:")
                     print(f"Yellow: {round(p4_2.count("🟨") / len(p4_2) * 100, 1)}%")
                     print(f"Purple: {round(p4_2.count("🟪") / len(p4_2) * 100, 1)}%")
                     print(f"Orange: {round(p4_2.count("🟧") / len(p4_2) * 100, 1)}%")
                     print(f"Red: {round(p4_2.count("🟥") / len(p4_2) * 100, 1)}%")
                     print(f"Green: {round(p4_2.count("🟩") / len(p4_2) * 100, 1)}%")
                     print(f"Brown: {round(p4_2.count("🟫") / len(p4_2) * 100, 1)}%")
                     print(f"Black: {round(p4_2.count("⬛") / len(p4_2) * 100, 1)}%")
                     print(f"Blue: {round(p4_2.count("🟦") / len(p4_2) * 100, 1)}%")
                     print(f"White: {round(p4_2.count("⬜") / len(p4_2) * 100, 1)}%")
                     print(f"Sword: {round(p4_2.count("⚔️ ") / len(p4_2) * 100, 1)}%")
                     print()
                     print("Position 3:")
                     print(f"Yellow: {round(p4_3.count("🟨") / len(p4_3) * 100, 1)}%")
                     print(f"Purple: {round(p4_3.count("🟪") / len(p4_3) * 100, 1)}%")
                     print(f"Orange: {round(p4_3.count("🟧") / len(p4_3) * 100, 1)}%")
                     print(f"Red: {round(p4_3.count("🟥") / len(p4_3) * 100, 1)}%")
                     print(f"Green: {round(p4_3.count("🟩") / len(p4_3) * 100, 1)}%")
                     print(f"Brown: {round(p4_3.count("🟫") / len(p4_3) * 100, 1)}%")
                     print(f"Black: {round(p4_3.count("⬛") / len(p4_3) * 100, 1)}%")
                     print(f"Blue: {round(p4_3.count("🟦") / len(p4_3) * 100, 1)}%")
                     print(f"White: {round(p4_3.count("⬜") / len(p4_3) * 100, 1)}%")
                     print(f"Sword: {round(p4_3.count("⚔️ ") / len(p4_3) * 100, 1)}%")
                     print()
              else:
                     print("You messed up.")
              input("Press enter to continue")

def lose_and_win_check():
       global lose, win
       if mode == "S":
              if p1_stats[HEALTH_KEY] <= 0 or p2_stats[HEALTH_KEY] <= 0 or p3_stats[HEALTH_KEY] <= 0 or p4_stats[HEALTH_KEY] <= 0:
                     lose = True
                     print("You Lose!")
                     play_again()
              elif p1_stats[POINTS_KEY] == 10 and p2_stats[POINTS_KEY] == 10 and p3_stats[POINTS_KEY] == 10 and p4_stats[POINTS_KEY] == 10:
                     win = True
                     print("You win!")
                     play_again()
       elif mode == "M":
              if 1 in active_players and p1_stats[HEALTH_KEY] <= 0:
                     print("Player 1 has lost!")
                     active_players.remove(1)
                     input("Press enter to continue")
              if 2 in active_players and p2_stats[HEALTH_KEY] <= 0:
                     print("Player 2 has lost!")
                     active_players.remove(2)
                     input("Press enter to continue")
              if 3 in active_players and p3_stats[HEALTH_KEY] <= 0:
                     print("Player 3 has lost!")
                     active_players.remove(3)
                     input("Press enter to continue")
              if 4 in active_players and p4_stats[HEALTH_KEY] <= 0:
                     print("Player 4 has lost!")
                     active_players.remove(4)
                     input("Press enter to continue")

              if p1_stats[POINTS_KEY] == 10 and 1 not in winning_players:
                     winning_players.append(1)
              if p2_stats[POINTS_KEY] == 10 and 2 not in winning_players:
                     winning_players.append(2)
              if p3_stats[POINTS_KEY] == 10 and 3 not in winning_players:
                     winning_players.append(3)
              if p4_stats[POINTS_KEY] == 10 and 4 not in winning_players:
                     winning_players.append(4)

              if 1 in winning_players and (p1_stats[HEALTH_KEY] <= 0 or p1_stats[POINTS_KEY] < 10):
                     winning_players.remove(1)
              if 2 in winning_players and (p2_stats[HEALTH_KEY] <= 0 or p2_stats[POINTS_KEY] < 10):
                     winning_players.remove(2)
              if 3 in winning_players and (p3_stats[HEALTH_KEY] <= 0 or p3_stats[POINTS_KEY] < 10):
                     winning_players.remove(3)
              if 4 in winning_players and (p4_stats[HEALTH_KEY] <= 0 or p4_stats[POINTS_KEY] < 10):
                     winning_players.remove(4)

              if winning_players == active_players:
                     if len(winning_players) > 1:
                            print("Players " + ", ".join(str(player) for player in winning_players) + " have won!")
                     elif len(winning_players) == 1:
                            print("Player " + str(winning_players[0]) + " has won!")
                     elif len(winning_players) == 0:
                            print("All players have lost!")
                     play_again()


def play_again():
       global lose, win, p1_stats, p2_stats, p3_stats, p4_stats, enemy_min, enemy_max, p1_contamination, p2_contamination
       global p3_contamination, p4_contamination, p1_blind, p2_blind, p3_blind, p4_blind, active_players, winning_players
       print("Do you want to play again?")
       reset = input("Enter 'y' for yes or 'n' for no: ")
       if reset == "y" or reset == "Y":
              lose = False
              win = False
              p1_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
              p2_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
              p3_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
              p4_stats = {"Health":5, "Strength":5, "Gold":5, "Points":0}
              p1_contamination = []
              p2_contamination = []
              p3_contamination = []
              p4_contamination = []
              p1_blind = False
              p2_blind = False
              p3_blind = False
              p4_blind = False
              active_players = [1, 2, 3, 4]
              enemy_min = 1
              enemy_max = 5
              active_players = [1, 2, 3, 4]
              winning_players = []
              main()
       elif reset == "n" or reset == "N":
              print("Thanks for playing!")
              raise InterruptedError
       else:
              print("Invalid input. Please try again.")
              play_again()

def main():
       global p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r, mode, p1_1, p1_2, p1_3, p2_1, p2_2
       global p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3
       loopDone = False
       while loopDone == False:
              mode = input("Please select 'S' for single-player or 'M' for multiplayer: ")
              if mode == "S" or mode == "M":
                     loopDone = True
                     if mode == "M":
                            if  "⚔️ " in SQUARE_TYPES:
                                   pass
                            else:
                                   SQUARE_TYPES.append("⚔️ ")
                     if mode == "S":
                            if  "⚔️ " in SQUARE_TYPES:
                                   SQUARE_TYPES.remove("⚔️ ")
                            else:
                                   pass
              else:
                     print("Bad input. Please try again.")
       p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3 = game_reset()
       p1_1r, p1_2r, p1_3r, p2_1r, p2_2r, p2_3r, p3_1r, p3_2r, p3_3r, p4_1r, p4_2r, p4_3r = random_square(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
       if mode == "S":
              while lose == False and win == False:
                     choices(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)
       elif mode == "M":
              while lose == False and win == False:
                     multi_choice(p1_1, p1_2, p1_3, p2_1, p2_2, p2_3, p3_1, p3_2, p3_3, p4_1, p4_2, p4_3)

if __name__ == "__main__":
       main()