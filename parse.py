import csv
import datetime
import json
import time
import pandas as pd
import dota2api
api = dota2api.Initialise("4D871C3CC56D4E987911394AF8F6C021", raw_mode=True)
match_list = pd.read_csv("output.csv")
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

