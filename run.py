import csv
import datetime
import json
import time
import pandas as pd
import numpy as np
import dota2api
api = dota2api.Initialise("4D871C3CC56D4E987911394AF8F6C021", raw_mode=True)


live_games_array = np.zeros(1)

# When called, function updates old live game list with new.
# Any game that gets replaced will be recorded in unparsed_output.csv
def update_live_games():
    print(live_games_array)
    # pull game information
    print("pulling game information")
    live_games = api.get_top_live_games()
    game_count=len(live_games['game_list'])
    new_list = []
    
    # filter for mmr > 0
    for i in range(game_count):
        mmr = live_games['game_list'][i]['average_mmr']
        matchid = live_games['game_list'][i]['match_id']
        matchtime = live_games['game_list'][i]['activate_time']
        matchinfo = [{'matchid': matchid, 'mmr': mmr, 'matchtime': matchtime}]
        
        if mmr > 0: 
            new_list.append(matchinfo)

    # convert to array for set comparison (assuming matchtime is unique and unchanged)
    new_array = np.asarray(new_list)
    print("new array is")
    print(new_array)

    # Return the sorted, unique values in ar1 that are not in ar2.
    update_list = np.setdiff1d(new_array, live_games_array)
    print("updated list is")
    print(update_list)

    # Record new games in csv file
    for i in range(len(update_list)):
        pd.DataFrame(update_list[i]).to_csv('unparsed_output.csv', mode='a', header=False)

    # Update array for next function call
    live_games_array = new_array
    print("updated since")
    print(datetime.datetime.now())
    return

while True:
        try:
            print("updating")
            update_live_games()
        except:
            pass
        print("waiting for 10 seconds")
        time.sleep(10)
