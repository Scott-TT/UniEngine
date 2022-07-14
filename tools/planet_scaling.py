import random 
import math
import time

from pprint import pprint

import planet_item
import economy_config
import defense_scaling
import fleet_scaling

class PlanetScaling:
    def __init__(self, config=None):
        if config == None:
            self.config = {
                "universe_production_multiplier": economy_config.production_multiplier
                ,"level_mines_min"              : 3
                ,"level_mines_max"              : 42
                ,"level_storage_min"            : 0
                ,"level_storage_max"            : 30
                ,"production_time_min"          : 24
                ,"production_time_max"          : 24*365*10
                ,"linear_to_exponential_scaling": (lambda x: x * math.exp(2*(math.pow(x,2)-1)))
                ,"fleet_on_planet_proba"        : (lambda x: random.randint(0,100) < 50-2*x)
                ,"fleet_worth_multiplier"       : (lambda  : random.randint(50,100)/100)
                ,"defenses_worth_multiplier"    : (lambda  : random.randint(40,100)/100)
            }

    def compute_scaling_factor(self, planet=None, linear_scaling_level=None, mode=None):
        linear_scaling = 0
        if linear_scaling_level is None:
            if planet is None:
                raise
             # Compute base level
            linear_scaling = (planet.parameters["galaxy"]-1)*10 \
                            + min(400,max(100,planet.parameters["system"]))*20/400
            linear_scaling /= 100
            # Throw in some noise
            if linear_scaling < 1:
                linear_scaling *= random.gauss(1,0.2)
                linear_scaling += random.gauss(0,0.1) # Can be negative
            # Clamp to [0-1]
            linear_scaling = min(1,max(0,linear_scaling))
        else:
            linear_scaling = linear_scaling_level

        result = 0
        if mode == None or mode == "linear":
            result = linear_scaling
        elif mode == "exponential":
            result = self.config["linear_to_exponential_scaling"](linear_scaling)

        return min(1,max(0,result))
    
    def compute_total_production_per_hour(self, planet, universe_production_multiplier=1):
        if universe_production_multiplier == None:
            universe_production_multiplier = self.config["universe_production_multiplier"]
        total = 0
        for b in ["metal_mine","crystal_mine","deuterium_synthesizer"]: 
            mine_level = planet[b]
            total = total + 20 * mine_level * 1.1**mine_level
        total = universe_production_multiplier * total
        return math.floor(total)
    
    def compute_planet_juice(self, scaling_level, planet):
        scaling_linear = self.compute_scaling_factor(linear_scaling_level=scaling_level, mode="linear")
        scaling_exp    = self.compute_scaling_factor(linear_scaling_level=scaling_level, mode="exponential")
        seniority  = scaling_exp * self.config["production_time_max"]
        juice = self.compute_total_production_per_hour(planet) * ( seniority + self.config["production_time_min"])
        juice = math.floor(juice)
        return juice

    def compute_static_defenses(self, planet, scaling_level):
        defense_juice = self.compute_planet_juice(scaling_level, planet) * self.config["defenses_worth_multiplier"]()
        scaler = defense_scaling.get_random_profile()
        scaler.fill_defenses(planet=planet, juice=defense_juice)

    def compute_fleets(self, planet, scaling_level):
        if not self.config["fleet_on_planet_proba"](scaling_level):
            return
        fleet_juice = self.compute_planet_juice(scaling_level, planet) * self.config["fleet_worth_multiplier"]()
        scaler = fleet_scaling.get_random_profile()
        scaler.fill_fleets(planet=planet, juice=fleet_juice)

    def compute_mines_level(self, planet, scaling_level):
        scaling_factor = self.compute_scaling_factor(linear_scaling_level=scaling_level, mode="linear")
        planet["solar_plant"] = 1
        for mine in ["metal_mine","crystal_mine","deuterium_synthesizer"]:
            c = self.config["level_mines_max"]
            m1 = max(1,self.config["level_mines_min"])
            a = (c-m1)/m1
            x = scaling_factor
            b = 5.5
            average = c / ( 1 + a * math.exp(-b*x))
            blevel = random.gauss(average,2)
            blevel = max(0,min(50,blevel))
            planet[mine] = math.floor(blevel)
            planet["solar_plant"] = max(planet["solar_plant"], planet[mine])

    def compute_storage_level(self, planet, scaling_level):
        scaling_factor = self.compute_scaling_factor(linear_scaling_level=scaling_level, mode="linear")
        for storage in ["metal_storage","crystal_storage","deuterium_tank"]:
            c = self.config["level_storage_max"]
            m1 = max(1,self.config["level_storage_min"])
            a = (c-m1)/m1
            x = scaling_factor
            b = 5.5
            average = c / ( 1 + a * math.exp(-b*x))
            blevel = random.gauss(average,math.ceil(average/12))
            blevel = max(0,min(50,blevel))
            planet[storage] = math.floor(blevel)

    def generate_planet_buildings(self, scaling_level):
        planet = {}
        self.compute_mines_level(planet=planet, scaling_level=scaling_level)
        self.compute_storage_level(planet=planet, scaling_level=scaling_level)
        self.compute_static_defenses(planet=planet, scaling_level=scaling_level)
        self.compute_fleets(planet=planet, scaling_level=scaling_level)

        return planet
