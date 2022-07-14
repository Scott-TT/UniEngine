import random 
import randomname
import math
import time

from pprint import pprint

import economy_config
import planet_item
import planet_scaling
import player_scaling

class Planet:

    def __init__(self, galaxy, system, planet, owner_id=None, empty_shell=False):
        self.parameters = {
            "Name" : randomname.get_name()
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
        self.scaling_level = self.generator.compute_scaling_factor(planet=self)
        self.init_geo()
        if empty_shell:
            return
        self.init_buildings()
        self.init_resources_values()
        if owner_id == None:
            players = player_scaling.PlayerScaling()
            planet_juice = self.generator.compute_planet_juice(scaling_level=self.scaling_level, planet=self.parameters)
            new_owner = players.get_suitable_player(target=planet_juice)
            self.assign_to_player(new_owner.id)
        else:
            self.assign_to_player(owner_id)

    def assign_to_player(self, user_id):
        self.parameters["id_owner"] = user_id

    def init_resources_values(self):
        # Hourly income computation
        self.parameters["metal_perhour"]     = 30 * economy_config.production_multiplier * self.parameters["metal_mine"]**1.1
        self.parameters["crystal_perhour"]   = 20 * economy_config.production_multiplier * self.parameters["crystal_mine"]**1.1
        self.parameters["deuterium_perhour"] = 12 * economy_config.production_multiplier * self.parameters["deuterium_synthesizer"]**1.1

        # Initial stock of one week worth of production
        self.parameters["metal"]     = self.parameters["metal_perhour"] * 24*7
        self.parameters["crystal"]   = self.parameters["crystal_perhour"] * 24*7
        self.parameters["deuterium"] = self.parameters["deuterium_perhour"] * 24*7

        # Compute and apply maximum storage capacity
        self.parameters["metal_max"] = 100000 * math.pow(1.7,self.parameters["metal_storage"])
        self.parameters["metal"] = min(self.parameters["metal"], self.parameters["metal_max"])
        self.parameters["crystal_max"] =  100000 * math.pow(1.7,self.parameters["crystal_storage"])
        self.parameters["crystal"] = min(self.parameters["crystal"], self.parameters["crystal_max"])
        self.parameters["deuterium_max"] =  100000 * math.pow(1.7,self.parameters["deuterium_tank"])
        self.parameters["deuterium"] = min(self.parameters["deuterium"], self.parameters["deuterium_max"])
  
    def init_buildings(self):
        self.parameters = { **self.parameters, **self.generator.generate_planet_buildings(self.scaling_level) }

    def print_debug (self, display_scaling=False, display_fleet=False, display_defenses=False):
        scale = planet_scaling.PlanetScaling()
        ships = {k:v for k,v in self.parameters.items() if k in planet_item.fleets }
        defenses = {k:v for k,v in self.parameters.items() if k in planet_item.buildings }
        if display_scaling:
            print("Scaling factor of (%d,%d,%d) : \
\n  linear=%f \n  exponential=%f\n  juice=>%s"
                                                   % (self.parameters["galaxy"],self.parameters["system"],self.parameters["planet"]
                                                    ,scale.compute_scaling_factor(linear_scaling_level=self.scaling_level)
                                                    ,scale.compute_scaling_factor(linear_scaling_level=self.scaling_level, mode="exponential")
                                                    ,f'{scale.compute_planet_juice(self.scaling_level, self.parameters):,}'
                                                   ))
        if display_fleet:
            print("Ships:")
            pprint(ships)
            cost = 0
            for type, quantity in ships.items():
                cost += planet_item.fleets[type].total_cost() * quantity
            print("  Total cost : %s" % f"{cost:,}")
        if display_defenses:
            print("Defenses:")
            pprint(defenses)
            cost = 0
            for type, quantity in defenses.items():
                cost += planet_item.buildings[type].total_cost() * quantity
            print("  Total cost : %s" % f"{cost:,}")
  
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
