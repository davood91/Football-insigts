import tkinter as tk
import pymysql

# database
connection = pymysql.connect(
    host='localhost',
    user='root',
    password='',
    db='ARGENTINA_WC',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor
)


window = tk.Tk()
window.title("Soccer Database")

window['background'] = 'blue'
label = tk.Label(window, text="Soccer database for team argentina, for assisting team coach ", font=("Arial", 14, "bold"))
label.pack()


player_frame = tk.Frame(window)
player_frame.pack()

# Create a label and option menu for player details
player_label = tk.Label(player_frame, text="Player details:")
player_label.pack(side='left')
player_option = tk.StringVar(player_frame)
player_option.set("Select option") # default value
player_menu = tk.OptionMenu(player_frame, player_option, "Order by age", "Order by player ID", "No. of goals", "No. of man of the matches", "No. of saves")
player_menu.pack(side='left')


best_frame = tk.Frame(window)
best_frame.pack()
# Create a label and option menu for best selection
best_label = tk.Label(best_frame, text="Best selection:")
best_label.pack(side='left')
best_option = tk.StringVar(best_frame)
best_option.set("Select option") # default value
best_menu = tk.OptionMenu(best_frame, best_option, "Best player (most man of the matches)", "Best boot (most goals)", "Best play maker (most assists)", "Best goal keeper (most saves)")
best_menu.pack(side='left')
# Create a frame for the match details selection box
match_frame = tk.Frame(window)
match_frame.pack()


match_label = tk.Label(match_frame, text="Match details:")
match_label.pack(side='left')
match_option = tk.StringVar(match_frame)
match_option.set("Select option") # default value
match_menu = tk.OptionMenu(match_frame, match_option, "All matches", "Won matches", "Lost matches")
match_menu.pack(side='left')


stats_frame = tk.Frame(window)
stats_frame.pack()

# Create a label and option menu for average statistics
stats_label = tk.Label(stats_frame, text="Average statistics:")
stats_label.pack(side='left')
stats_option = tk.StringVar(stats_frame)
stats_option.set("Select option") # default value
stats_menu = tk.OptionMenu(stats_frame, stats_option, "Average goals", "Average assists", "Average possession", "Average shots on target", "Average shots")
stats_menu.pack(side='left')


button_frame = tk.Frame(window)
button_frame.pack()


def on_button_click():
    # Retrieve the selected options from the option menus
    player_selected = player_option.get()
    best_selected = best_option.get()
    match_selected = match_option.get()
    stats_selected = stats_option.get()
    
    
    with connection.cursor() as cursor:
        if player_selected == "Order by age":
            sql = "SELECT * FROM PLAYERS ORDER BY age"
        elif player_selected == "Order by player ID":
            sql = "SELECT * FROM PLAYERS ORDER BY player_id"
        elif player_selected == "No. of goals":
            sql = "SELECT * FROM PLAYERS ORDER BY goals DESC"
        elif player_selected == "No. of man of the matches":
            sql = "SELECT * FROM PLAYERS ORDER BY no_of_man_of_the_matches DESC"
        elif player_selected == "No. of saves":
            sql = "SELECT * FROM PLAYERS ORDER BY saves DESC"
        elif best_selected == "Best player (most man of the matches)":
            sql = "SELECT player_id, name_ as best_player,max(no_of_man_of_the_matches) as man_of_the_matches FROM PLAYERS WHERE no_of_man_of_the_matches = (SELECT max(no_of_man_of_the_matches) FROM PLAYERS)"
        elif best_selected == "Best boot (most goals)":
            sql = "SELECT player_id,name_ as best_boot, max(goals)  as total_goals FROM PLAYERS WHERE goals = (SELECT max(goals) FROM PLAYERS)"
        elif best_selected == "Best play maker (most assists)":
            sql = "SELECT player_id,name_ as best_boot, max(assist)  as total_assists FROM PLAYERS WHERE assist = (SELECT max(assist) FROM PLAYERS)"
        elif best_selected ==  "Best goal keeper (most saves)":
         sql = "SELECT player_id,name_ as best_goalkeeper,  max(saves) as total_saves FROM PLAYERS WHERE saves = (SELECT max(saves) FROM PLAYERS)"
        elif match_selected == "All matches":
            sql = "SELECT * FROM GAMES"
        elif match_selected == "Won matches":
            sql = "SELECT * FROM GAMES WHERE result = 'WIN'"
        elif match_selected == "Lost matches":
            sql = "SELECT * FROM GAMES WHERE result = 'LOSS'"
        elif stats_selected == "Average goals":
            sql = "SELECT AVG(goals) as average_goals FROM PLAYERS"
        elif stats_selected == "Average assists":
            sql = "SELECT AVG(assist) as average_assists FROM PLAYERS"
        elif stats_selected == "Average possession":
            sql = "SELECT AVG(possession) as average_possession FROM STATS"
        elif stats_selected == "Average shots on target":
            sql = "SELECT AVG(shots_on_target) as average_shots_on_target FROM STATS"
        elif stats_selected == "Average shots":
            sql = "SELECT AVG(shots) as average_shots FROM STATS"
        cursor.execute(sql)
        result = cursor.fetchall()
    

    result_label['text'] = ""
    
    # Print the retrieved data in the result label
    for row in result:
        result_label['text'] += str(row) + "\n"


button = tk.Button(button_frame, text="Retrieve data", command=on_button_click)
button.pack()

result_label = tk.Label(window)
result_label.pack()

def clear_screen():
    # Clear the label's text
    result_label['text'] = ''

# Create the button
clear_button = tk.Button(button_frame, text="Clear", command=clear_screen)
clear_button.pack(side='left')


window.mainloop()
