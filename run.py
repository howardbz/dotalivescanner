import csv
import datetime
import json
import time
import pandas as pd
import numpy as np
import dota2api

# Created our own libraries

import analysis.update as upd

upd.init()

while True:
        try:
            print("updating")
            upd.update_live_games()
            print("parsing old games")
            upd.parse_games()
        except:
            pass
        print("waiting for 10 minutes")
        time.sleep(600)

# print("updating")
# update_live_games(live_games_array)
