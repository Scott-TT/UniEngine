import pymysql
import random

import database_config
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

bot1 = player_scaling.Player("Bob",2500)
player_gen = populate_players.PopulatePlayers(cursor)
player_gen.insert(bot1)

galaxy_gen = populate_planets.PopulatePlanets(cursor, planet_probability_expression=(lambda g,s,p: random.randint(0,10000000) < 30))
galaxy_gen.populate_everything(depopulate=False)

cursor.close()                          
cnx.commit()
