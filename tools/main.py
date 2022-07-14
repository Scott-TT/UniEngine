import pymysql
import random
import sys

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
    galaxy_gen.populate_planets(in_place=False, remove_existing=True)

def generate_everything_anew():
    generate_all_players()
    generate_all_planets()

# Updates existing bot planets, without altering overall galaxy state
def regenerate_bot_planets():
    generate_all_players()
    galaxy_gen = populate_planets.PopulatePlanets( cursor )
    galaxy_gen.populate_planets(in_place=True)


if len(sys.argv) == 2:
    if sys.argv[1] == "--full":
        generate_everything_anew()
    elif sys.argv[1] == "--regenerate":
        regenerate_bot_planets()
else:
    for (g,s,p) in [ (g,s,p) for g in range(1,5) for s in range(1,500,999) for p in range(1,16,999) ]:
        p = planet.Planet(galaxy=g, system=s, planet=p)
        p.print_debug(display_defenses=True, display_scaling=True)
        print()

cursor.close()                 
cnx.commit()
