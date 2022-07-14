import pymysql
import random

from pprint import pprint

import database_config
import defense_scaling
import fleet_scaling
import planet
import planet_scaling
import player_scaling
import populate_planets
import populate_players

db_config = database_config.default_config
cnx = pymysql.connect(user = db_config.user
                        ,password = db_config.password
                        ,host = db_config.host
                        ,database = db_config.database
                        )
cursor = cnx.cursor()

def generate_all_players():
    player_gen = populate_players.PopulatePlayers(cursor)
    player_gen.populate_players()

def generate_all_planets():
    galaxy_gen = populate_planets.PopulatePlanets( cursor
                                                  ,planet_probability_expression=(lambda g,s,p: random.randint(0,100) < 42)
                                                  )
    galaxy_gen.populate_everything(depopulate_clause="WHERE id_owner NOT IN (SELECT id FROM _users WHERE isAI=0)")

def generate_everything():
    generate_all_players()
    generate_all_planets()

# Updates existing bot planets, without altering overall galaxy state
def regenerate_planets():
    galaxy_gen = populate_planets.PopulatePlanets( cursor
                                                  ,populate_planets.retrieve_existing_planets_coordinates(cursor=cursor, only_bots=True)
                                                  )

if False:
    generate_everything()

if False:
    regenerate_planets()

cursor.close()                 
cnx.commit()
