import csv
import datetime
import json
import time
import pandas as pd
import dota2api
api = dota2api.Initialise("4D871C3CC56D4E987911394AF8F6C021", raw_mode=True)
while True:
        try:
                live_games = api.get_top_live_games()
                game_count=len(live_games['game_list'])
                old_games = pd.read_csv("output.csv")
                for i in range(0,game_count):
                        mmr = live_games['game_list'][i]['average_mmr']
                        matchid = live_games['game_list'][i]['match_id']
                        matchtime= live_games['game_list'][i]['activate_time']
                        matchinfo = [{'matchid': matchid, 'mmr': mmr, 'matchtime': matchtime}]
                        ismatch = matchid in set(old_games['Match Id'])
                        print(mmr)
                        print(matchid in set(old_games['Match Id']))
                        if mmr > 0:
                                if  not ismatch:
                                        print(matchinfo)
                                        pd.DataFrame(matchinfo).to_csv('output.csv', mode='a', header=False)
                print(datetime.datetime.now())
                time.sleep(600)
        except:
            pass
