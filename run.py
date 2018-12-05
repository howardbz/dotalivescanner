import csv
import datetime
import json
import time
import pandas as pd
import numpy as np
import dota2api
api = dota2api.Initialise("4D871C3CC56D4E987911394AF8F6C021", raw_mode=True)


live_games_list = []

# When called, function updates old live game list with new.
# Any game that gets replaced will be recorded in unparsed_output.csv
def update_live_games():
    global live_games_list
    print(live_games_list)
    # pull game information
    print("pulling game information")
    live_games = api.get_top_live_games()
    game_count=len(live_games['game_list'])
    new_list = []
    update_list = []
    
    for i in range(game_count):
        mmr = live_games['game_list'][i]['average_mmr']
        matchid = live_games['game_list'][i]['match_id']
        matchtime = live_games['game_list'][i]['activate_time']
        matchinfo = [{'matchid': matchid, 'mmr': mmr, 'matchtime': matchtime}]

        if mmr > 0:
            # if matchid exists in previous array, is repeated match, retain entry in next call
            if matchid in live_games_list:
                new_list.append(matchid)
            # if matchid doesn't exist, is new match, put entry in next call and record in csv
            else:
                pd.DataFrame(matchinfo).to_csv('unparsed_output.csv', mode='a', header=False)
                new_list.append(matchid)
                update_list.append(matchid)
            # if matchid existed in previous array but isn't queried, deleted from next call automatically

    # convert to array and update live games array for next call comparison
    live_games_list = new_list
    print("new live games array is")
    print(live_games_list)

    print("updated list is")
    print(update_list)

    print("updated since")
    print(datetime.datetime.now())
    return

while True:
        try:
            print("updating")
            update_live_games()
        except:
            pass
        print("waiting for 10 minutes")
        time.sleep(600)

# print("updating")
# update_live_games(live_games_array)

