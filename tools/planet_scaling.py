import random 
import math
import time

metal_cost_ratio = 1
crystal_cost_ratio = 1.5
deut_cost_ratio = 2.5

class DefenseItem:
    def __init__(self, metal, crystal, deut, maximum_quantity=None):
        self.metal = metal
        self.crystal = crystal
        self.deut = deut
        self.maximum_quantity = maximum_quantity
        self.juice = math.floor(metal*metal_cost_ratio + crystal*crystal_cost_ratio + deut*deut_cost_ratio)

class DefenseConfig:
  buildings = {
     "rocket_launcher"       : DefenseItem(metal=2000  ,crystal=0     ,deut=0     ,maximum_quantity=None)
    ,"light_laser"           : DefenseItem(metal=1500  ,crystal=500   ,deut=0     ,maximum_quantity=None)
    ,"heavy_laser"           : DefenseItem(metal=6000  ,crystal=2000  ,deut=0     ,maximum_quantity=None)     
    ,"gauss_cannon"          : DefenseItem(metal=20000 ,crystal=15000 ,deut=2000  ,maximum_quantity=None)
    ,"ion_cannon"            : DefenseItem(metal=3000  ,crystal=5000  ,deut=0     ,maximum_quantity=None)   
    ,"plasma_turret"         : DefenseItem(metal=50000 ,crystal=50000 ,deut=30000 ,maximum_quantity=None)
    ,"small_shield_dome"     : DefenseItem(metal=10000 ,crystal=10000 ,deut=0     ,maximum_quantity=1)
    ,"large_shield_dome"     : DefenseItem(metal=50000 ,crystal=50000 ,deut=0     ,maximum_quantity=1)
    ,"antiballistic_missile" : DefenseItem(metal=12500 ,crystal=2500  ,deut=10000 ,maximum_quantity=300) 
  }
  
  fleets = {
     "small_cargo_ship" : DefenseItem(metal=2000    ,crystal=2000    ,deut=0       )
    ,"big_cargo_ship"   : DefenseItem(metal=6000    ,crystal=6000    ,deut=0       )      
    ,"light_fighter"    : DefenseItem(metal=3000    ,crystal=1000    ,deut=0       )
    ,"heavy_fighter"    : DefenseItem(metal=6000    ,crystal=4000    ,deut=0       )
    ,"cruiser"          : DefenseItem(metal=20000   ,crystal=7000    ,deut=2000    )
    ,"battleship"       : DefenseItem(metal=45000   ,crystal=15000   ,deut=0       ) 
    ,"battlecruiser"    : DefenseItem(metal=30000   ,crystal=40000   ,deut=15000   )
    ,"recycler"         : DefenseItem(metal=10000   ,crystal=6000    ,deut=2000    )
    ,"bomber"           : DefenseItem(metal=50000   ,crystal=25000   ,deut=15000   )
    ,"destroyer"        : DefenseItem(metal=60000   ,crystal=50000   ,deut=15000   )
    ,"deathstar"        : DefenseItem(metal=5000000 ,crystal=4000000 ,deut=1000000 )
  }

class PlanetScaling:
 
    def __init__(self, config=None):
        if config == None:
            self.config = {
                "universe_production_multiplier"    : 10
                ,"distance_max"           : 7*500
                ,"distance_max_defenses"  : 1500
                ,"level_mines_min"        : 6
                ,"level_mines_max"        : 40
                ,"level_storage_min"      : 0
                ,"level_storage_max"      : 13
            }

    def compute_scaling_factor(self, distance, mode=None):
        linear_scaling = max(0,min(1, distance / self.config["distance_max"]))
        if mode == None or mode == "linear":
            return linear_scaling
        elif mode == "exponential":
            x = linear_scaling
            return x * math.exp(2.1*(math.pow(x,2)-1))
    
    def compute_total_production(self, planet, universe_production_multiplier=1):
        if universe_production_multiplier == None:
            universe_production_multiplier = self.config["universe_production_multiplier"]
        total = 0
        for b in ["metal_mine","crystal_mine","deuterium_synthesizer"]: 
            mine_level = planet[b]
            total = total + 20 * mine_level * 1.1**mine_level
        total = universe_production_multiplier * total
        return math.floor(total)
    
    def compute_planet_juice(self, distance, planet):
        distance_scaling_factor = self.compute_scaling_factor(distance, mode="exponential")
        seniority_days_factor  = distance_scaling_factor * 365 * 24                        # Up to one year of linear scaling
        seniority_days_factor += math.floor(min(7, max(distance/10*7,0))) * 24             # Most planets have at least one week
        juice = self.compute_total_production(planet) * seniority_days_factor 
        juice = math.floor(juice)
        return juice
  
    def generate_planet_buildings(self, distance, scaling_factor = None):
        if scaling_factor == None:
            scaling_factor = self.compute_scaling_factor(distance)
        planet = {}
        planet["solar_plant"] = 1
        # Mines
        for b in ["metal_mine","crystal_mine","deuterium_synthesizer"]:
            m2 = self.config["level_mines_max"]
            m1 = self.config["level_mines_min"]
            average = self.config["level_mines_min"] + scaling_factor * (math.log(math.exp(m2-m1)-math.exp(m1)))
            blevel = random.gauss(average,2+average/6)
            blevel = max(0,min(50,blevel))
            planet[b] = math.floor(blevel)
            planet["solar_plant"] = max(planet["solar_plant"], planet[b])
      
        # Storages
        for b in ["metal_storage","crystal_storage","deuterium_tank"]:
            m2 = self.config["level_storage_max"]
            m1 = self.config["level_storage_min"]
            average = self.config["level_storage_min"] + scaling_factor * (math.log(math.exp(m2-m1)-math.exp(m1)))
            blevel = random.gauss(average,average/12)
            blevel = max(0,min(50,blevel))
            planet[b] = math.floor(blevel)
      
        # Static defenses
        defense_juice = self.compute_planet_juice(distance, planet) * random.randint(40,100)/100 # Not everyone builds defenses
        defense_buildings = {k: v for k,v in DefenseConfig.buildings.items() if v.juice < defense_juice }
        total_value_per_item = defense_juice / max(1,len(defense_buildings))
        for k,v in defense_buildings.items():
            quantity = math.floor(total_value_per_item / v.juice * random.randint(50,200)/100)
            if v.maximum_quantity:
                quantity = min(v.maximum_quantity,quantity)
            if quantity > 0:
                planet[k] = quantity
      
      
        # Fleets
        fleet_juice = self.compute_planet_juice(distance, planet)# 
        fleet_ships = {k: v for k,v in DefenseConfig.fleets.items() if v.juice < fleet_juice }
        total_value_per_item = fleet_juice / max(1,len(fleet_ships))
        for k,v in fleet_ships.items():
            quantity = math.floor(total_value_per_item / v.juice * random.gauss(80,20) / 100)
            if quantity > 0:
                planet[k] = quantity
    
    
        # Actual juice
        planet["metal_perhour"]     = 30 * self.config["universe_production_multiplier"] * planet["metal_mine"]**1.1
        planet["crystal_perhour"]   = 20 * self.config["universe_production_multiplier"] * planet["crystal_mine"]**1.1
        planet["deuterium_perhour"] = 12 * self.config["universe_production_multiplier"] * planet["deuterium_synthesizer"]**1.1
    
        planet["metal"]     = planet["metal_perhour"] * 24*7
        planet["crystal"]   = planet["crystal_perhour"] * 24*7
        planet["deuterium"] = planet["deuterium_perhour"] * 24*7
        return planet
