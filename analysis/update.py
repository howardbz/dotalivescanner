# Dota Live Scanner
# Howard Wang, Miles Wang

# Created on: 12/20/2018
# Last edited: 

# Repository for all update functions called upon by other functions.

import csv
import datetime
import json
import time
import pandas as pd
import numpy as np
import dota2api

# Declares any initial settings

def init():
    live_games_list = []
    api = dota2api.Initialise("4D871C3CC56D4E987911394AF8F6C021", raw_mode=True)
    return

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
                pd.DataFrame(matchinfo).to_csv('unparsed_output.csv', mode='a', header=False, index=False)
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


def parse_games():
        match_list = pd.read_csv("unparsed_output.csv")
        parsed_games = pd.read_csv("output_parsed.csv")
        match_len = len(match_list["Match Id"])
        parsed_len = len(parsed_games["Match Id"])

        if match_len > parsed_len:
                for i in range(parsed_len,match_len):
                        matchinfo = [{'matchid': match_list["Match Id"][i], 'mmr': match_list["MMR"][i], 'matchtime': match_list["Time"][i]}]
                        pd.DataFrame(matchinfo).to_csv('output_parsed.csv', mode='a', header=False, index=False)

        parsed_games = pd.read_csv("output_parsed.csv")           

        for i in range (0, len(parsed_games["Match Id"])):
                if str(parsed_games["Radiant_win"][i]).lower()!="true":
                        if str(parsed_games["Radiant_win"][i]).lower()!="false":
                                print("game " + str(i))
                                try:
                                        match = api.get_match_details(match_id=parsed_games["Match Id"][i])
                                        parsed_games["Radiant_win"][i] = match["radiant_win"]
                                        print(match["radiant_win"])
                                        for j in range (0, 10):
                                                parsed_games["Player_"+str(j+1)][i] = match['players'][j]['hero_id']
                                                print(match['players'][j]['hero_id'])
                                                
                                        for j in range (0,len(match['picks_bans'])):
                                                parsed_games["Bans_"+str(j+1)][i] = match['picks_bans'][j]['hero_id']
                                                print(match['picks_bans'][j]['hero_id'])
                                except:
                                        pass
                                
        pd.DataFrame(parsed_games).to_csv('output_parsed.csv', header=True, index=False)
        return