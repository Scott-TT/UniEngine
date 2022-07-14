import pymysql
import random 
import randomname
import math
import time
import pprint

from planet import Planet



class PopulatePlanets():
    def __init__(self, cursor, planet_probability_expression=None):
        self.cursor = cursor
        if planet_probability_expression is None:
            self.planet_probability_expression = (lambda g,s,p: random.randint(0,100) < 30)
        else:
            self.planet_probability_expression = planet_probability_expression

    def retrieve_existing_planets_coordinates(self, only_bots=None):
        if only_bots is None:
            only_bots = False
        sql = "SELECT galaxy, system, planet FROM _planets"
        if only_bots == True:
            # We exclude players instead of including bots
            sql += " WHERE id_owner NOT IN (SELECT id FROM _users WHERE isAI=0)"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_planet(self, p): 
        values_placeholder = ', '.join(['%s'] * len(p.parameters))
        columns = ', '.join(p.parameters.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_planets", columns, values_placeholder)
        self.cursor.execute(sql, list(p.parameters.values()))
  
        galaxy_entry = { "id_planet" : self.cursor.lastrowid }
        for k in ["galaxy", "system", "planet"]:
            galaxy_entry[k] = p.parameters[k]
        values_placeholder = ', '.join(['%s'] * len(galaxy_entry))
        columns = ', '.join(galaxy_entry.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_galaxy", columns, values_placeholder)
        self.cursor.execute(sql, list(galaxy_entry.values()))

    def upsert_planet(self, p):
        sql = f'DELETE FROM _planets WHERE galaxy={p.parameters["galaxy"]} AND system={p.parameters["system"]} AND planet={p.parameters["planet"]}'
        self.cursor.execute(sql)
        sql = f'DELETE FROM _galaxy WHERE galaxy={p.parameters["galaxy"]} AND system={p.parameters["system"]} AND planet={p.parameters["planet"]}'
        self.cursor.execute(sql)
        self.insert_planet(p)

    def delete_bots_planets(self):
        sql=f"DELETE FROM _planets WHERE id_owner NOT IN (SELECT id FROM _users WHERE isAI=0)"
        self.cursor.execute(sql)
        sql="DELETE FROM _galaxy WHERE id_planet NOT IN (SELECT id from _planets)"
        self.cursor.execute(sql)

    def create_planets(self):
        blacklist_coordinates = self.retrieve_existing_planets_coordinates()
        for (g,s,p) in [ (g,s,p) for g in range(1,10) for s in range(1,500) for p in range(1,16) ]:
            if self.planet_probability_expression(g,s,p) and (g,s,p) not in blacklist_coordinates:
                self.insert_planet(Planet(galaxy=g, system=s, planet=p))

    def populate_planets(self, in_place=True, remove_existing=False):
        if in_place == False:
            if remove_existing == True:
                self.delete_bots_planets()
            self.create_planets()
        else:
            planets_to_regenerate = self.retrieve_existing_planets_coordinates(only_bots=True)
            for (g,s,p) in planets_to_regenerate:
                self.upsert_planet(Planet(galaxy=g, system=s, planet=p))

