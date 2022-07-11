import random 
import randomname
import math
import time

import pprint
import planet_scaling

class Planet:

    def __init__(self, galaxy, system, planet):
        self.parameters = {
            "Name" : randomname.get_name()
            ,"id_owner" : 2
            ,"galaxy" : galaxy
            ,"system" : system
            ,"planet" : planet
            ,"planet_type" : 1
            ,"last_update" : time.time()
            ,"techQueue" : 0
            ,"buildQueue" : 0
            ,"shipyardQueue" : 0
        }
        self.generator = planet_scaling.PlanetScaling()
        self.planet = planet
        self.distance = max(0, system + (galaxy-1)*500)
        self.init_geo()
        self.init_buildings()
        self.init_resources_values()

    def init_resources_values(self): 
        self.parameters["metal_max"] = 100000 + 5000 * ( 2.5 * math.exp(20/33 * self.parameters["metal_storage"]))
        self.parameters["metal"] = min(self.parameters["metal"], self.parameters["metal_max"])
        self.parameters["crystal_max"] = 100000 + 5000 * ( 2.5 * math.exp(20/33 * self.parameters["crystal_storage"]))
        self.parameters["crystal"] = min(self.parameters["crystal"], self.parameters["crystal_max"])
        self.parameters["deuterium_max"] = 100000 + 50000 * ( 1.6 ** self.parameters["deuterium_tank"] - 1 )
        self.parameters["deuterium"] = min(self.parameters["deuterium"], self.parameters["deuterium_max"])
  
    def init_buildings(self):
        self.parameters = { **self.parameters, **self.generator.generate_planet_buildings(self.distance) }
    
    def print_defenses_and_fleets (self):
        ships = {k:v for k,v in self.parameters.items() if k in planet_scaling.DefenseConfig.fleets }
        defenses = {k:v for k,v in self.parameters.items() if k in planet_scaling.DefenseConfig.buildings }
        print()
        if True:
            print("Ships:")
            pprint.pprint(ships)
        if True:
            print("\nDefenses:")
            pprint.pprint(defenses)
  
    def init_geo(self):
        # sizes
        classic_base = 150
        setting_size = 250
        planet_ratio = math.floor((classic_base / setting_size) * 10000) / 100;
        random_min = [90, 125, 125, 205, 205, 205, 205, 205, 225, 205, 165, 155, 145, 80, 125]
        random_max = [91, 135, 135, 280, 280, 270, 220, 220, 230, 225, 180, 170, 200, 420, 190]
        calcul_min = math.floor(random_min[self.planet-1] + (random_min[self.planet - 1] * planet_ratio) / 100)
        calcul_max = math.floor(random_max[self.planet-1] + (random_max[self.planet - 1] * planet_ratio) / 100)
        random_size = random.randint(calcul_min,calcul_max)
        max_addon = random.randint(0, 110)
        min_addon = random.randint(0, 60)
        addon = max_addon - min_addon
        planet_fields = random_size + addon
        diameter = math.floor(math.sqrt(planet_fields) * 1000)
    
        # meteo
        planet_type = ""
        planet_design = ""
        planet_temp_min = 0
        if self.planet <= 3:
            planet_type = [ "trocken" ]
            planet_design = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10' ]
            planet_temp_min = random.randint(0, 100)
        elif self.planet <= 6:
            planet_type = [ "dschjungel" ]
            planet_design = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10' ]
            planet_temp_min = random.randint(-25,75)
        elif self.planet <= 9:
            planet_type = [ "normaltemp" ]
            planet_design = [ '01', '02', '03', '04', '05', '06', '07' ]
            planet_temp_min = random.randint(-50, 50)
      
        elif self.planet <= 12:
            planet_type = [ "wasser" ]
            planet_design = [ '01', '02', '03', '04', '05', '06', '07', '08', '09' ]
            planet_temp_min = random.randint(-75, 25)
      
        elif self.planet <= 15:
            planet_type = [ "eis" ]
            planet_design = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10' ]
            planet_temp_min = random.randint(-100, 10)
        else:
            planet_type = [ 'dschjungel', 'gas', 'normaltemp', 'trocken', 'wasser', 'wuesten', 'eis' ]
            planet_design = [ '01', '02', '03', '04', '05', '06', '07', '08', '09', '10' ]
            planet_temp_min = random.randint(-120, 10)
      
        planet_temp_maxi = random.randint(30, 100)
        planet_temp_max = planet_temp_min + planet_temp_maxi
      
        geo = {
            "field_max" : planet_fields
            ,"diameter" : diameter
            ,"image" : planet_type[random.randint(0, len(planet_type)-1)] + "planet" + planet_design[random.randint(0, len(planet_design)-1)]
            ,"temp_min" : planet_temp_min
            ,"temp_max" : planet_temp_max
            ,"metal" : 1000
            ,"metal_perhour" : 200
            ,"metal_max" : 100000
            ,"crystal" : 1000
            ,"crystal_perhour" : 200
            ,"crystal_max" : 100000
            ,"deuterium" : 200
            ,"deuterium_perhour" : 0
            ,"deuterium_max" : 100000
        }
      
        self.parameters = { **self.parameters, **geo }
