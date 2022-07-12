import pymysql
import random 
import randomname
import math
import time
import pprint

from planet import Planet

class PopulatePlanets():

    def __init__(self, cursor, existing_planets=None, planet_probability_expression=None):
        self.cursor = cursor
        if existing_planets is None:
            self.existing_planets = self.retrieve_existing_planets_coordinates()
        else:
            self.existing_planets = existing_planets

        if planet_probability_expression is None:
            self.planet_probability_expression = (lambda g,s,p: random.randint(0,100) < 30)
        else:
            self.planet_probability_expression = planet_probability_expression

    def retrieve_existing_planets_coordinates(self):  
        sql = "SELECT galaxy, system, planet FROM _planets"
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def insert_planet(self, p): 
        if (p.parameters["galaxy"], p.parameters["system"], p.parameters["planet"]) in self.existing_planets:
            return
  
        # Actual planet insertion
        values_placeholder = ', '.join(['%s'] * len(p.parameters))
        columns = ', '.join(p.parameters.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_planets", columns, values_placeholder)
        self.cursor.execute(sql, list(p.parameters.values()))
  
        # Galaxy reference chart
        galaxy_entry = { "id_planet" : self.cursor.lastrowid }
        for k in ["galaxy", "system", "planet"]:
            galaxy_entry[k] = p.parameters[k]
        values_placeholder = ', '.join(['%s'] * len(galaxy_entry))
        columns = ', '.join(galaxy_entry.keys())
        sql = "INSERT INTO %s ( %s ) VALUES ( %s )" % ("_galaxy", columns, values_placeholder)
        self.cursor.execute(sql, list(galaxy_entry.values()))
  
    def depopulate_everything(self, depopulate_clause):
        sql=f"DELETE FROM _planets {depopulate_clause}"
        self.cursor.execute(sql)
        sql="DELETE FROM _galaxy WHERE id_planet NOT IN (SELECT id from _planets)"
        self.cursor.execute(sql)
  
    def populate_system(self, galaxy, system):
        for i in range(1,16):
            if self.planet_probability_expression(galaxy, system, i):
                p = Planet(galaxy=galaxy, system=system, planet=i)
                self.insert_planet(p)

    def populate_galaxy(self, galaxy):
        for i in range(1,500):
            self.populate_system(galaxy=galaxy, system=i)

    def populate_everything(self, depopulate_clause="WHERE id < 0"):
        self.depopulate_everything(depopulate_clause)
        for i in range(1,10):
            self.populate_galaxy(galaxy=i)
