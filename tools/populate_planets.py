import pymysql
import random 
import randomname
import math
import time
import pprint

import database_config
from planet import Planet
from planet_scaling import PlanetScaling

db_config = database_config.default_config
cnx = pymysql.connect(user = db_config.user
                        ,password = db_config.password
                        ,host = db_config.host
                        ,database = db_config.database
                        )
cursor = cnx.cursor()

def retrieve_existing_planets_coordinates():  
    sql = "SELECT galaxy, system, planet FROM _planets"
    cursor.execute(sql)
    existing_planets = cursor.fetchall()
    return existing_planets

def insert_planet(p, existing_planets): 
    if (p.parameters["galaxy"], p.parameters["system"], p.parameters["planet"]) in existing_planets:
        return
  
    # Actual planet insertion
    values_placeholder = ', '.join(['%s'] * len(p.parameters))
    columns = ', '.join(p.parameters.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_planets", columns, values_placeholder)
    cursor.execute(sql, list(p.parameters.values()))
  
    # Galaxy reference chart
    galaxy_entry = { "id_planet" : cursor.lastrowid }
    for k in ["galaxy", "system", "planet"]:
        galaxy_entry[k] = p.parameters[k]
    values_placeholder = ', '.join(['%s'] * len(galaxy_entry))
    columns = ', '.join(galaxy_entry.keys())
    sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_galaxy", columns, values_placeholder)
    cursor.execute(sql, list(galaxy_entry.values()))
  
  
def depopulate_everything():
    sql="DELETE FROM _planets WHERE id > 2 AND id_owner=2"
    cursor.execute(sql)
    sql="DELETE FROM _galaxy WHERE galaxy_id>2 AND id_planet NOT IN (SELECT id from _planets)"
    cursor.execute(sql)
  
def populate_system(galaxy, system, coordinates_blacklist=[]):
    for i in range(1,16):
        if random.randint(0,100) < 30:
            p = planet(galaxy=galaxy, system=system, planet=i)
            insert_planet(p=p, existing_planets=coordinates_blacklist)

def populate_galaxy(galaxy, coordinates_blacklist=[]):
    for i in range(1,500):
        populate_system(galaxy=galaxy, system=i, coordinates_blacklist=coordinates_blacklist)

def populate_everything(depopulate=True, coordinates_blacklist=[]):
    if depopulate:
        depopulate_everything()
  
    for i in range(1,10):
        populate_galaxy(galaxy=i, coordinates_blacklist=coordinates_blacklist)

#populate_everything(coordinates_blacklist=retrieve_existing_planets_coordinates())
for i in range(10):
    print("\n--Galaxy %d--"%i)
    p = Planet(i,10,8)
    p.print_debug()

cursor.close()                          
cnx.commit()
