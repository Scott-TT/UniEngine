import pymysql
import random 
import randomname
import math
import string
import time
import pprint

import player_scaling

class PopulatePlayers():
    def __init__(self, cursor):
        self.cursor = cursor

    def cleanup_db(self):
        sql = "DELETE FROM _users WHERE isAI=1"
        self.cursor.execute(sql)

    def insert(self, player):
        player_db = { "username": player.name
                     ,"password": ''.join(random.choice(string.ascii_letters) for i in range(20))
                     ,"email": "bot@localhost"
                     ,"email_2": "nobot@localhost"
                     ,"isAI": 1
                     ,"avatar": "todo ?"
                     ,"user_lastip": "localhost"
                     ,"ip_at_reg": "localhost"
                     ,"user_agent": "bot"
                     ,"screen_settings": "2347_1320_24"
                     ,"current_page": "/UniEngine/buildings.php"
                     ,"skinpath": ""
                     ,"settings_FleetColors": ""
                     ,"ally_request_text":""
                     ,"activation_code":""
                     ,"new_pass":""
                     ,"new_pass_code":""
                     ,"old_username":""
                     ,"tasks_done":""
                     ,"achievements_unlocked":""
                }

        for tech,level in player.tech.tech.items():
            player_db["tech_%s"%tech] = level
        
        # Actual player insertion
        values_placeholder = ', '.join(['%s'] * len(player_db))
        columns = ', '.join(player_db.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_users  ", columns, values_placeholder)
        self.cursor.execute(sql, list(player_db.values()))

    def populate_players(self):
        self.cleanup_db()
        for p in player_scaling.all_players:
            self.insert(p)
            p.id = self.cursor.lastrowid
