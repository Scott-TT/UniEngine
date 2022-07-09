import pymysql
import random 
import randomname
import math
import time

#debug
import pprint
from functools import reduce
import database_config

db_config = database_config.default_config
cnx = pymysql.connect(user = db_config.user
                     ,password = db_config.password
                     ,host = db_config.host
                     ,database = db_config.database
                     )
                     
cursor = cnx.cursor()

query = "SELECT name, id_owner, galaxy, system, planet FROM _planets"
cursor.execute(query)

class defences:
  buildings = {
     "rocket_launcher"       : 2000
    ,"light_laser"           : 2000
    ,"heavy_laser"           : 8000     
    ,"gauss_cannon"          : 37000
    ,"ion_cannon"            : 8000   
    ,"plasma_turret"         : 130000
    ,"small_shield_dome"     : 20000
    ,"large_shield_dome"     : 100000
    ,"antiballistic_missile" : 10000 
  }
  
  fleets = {
     "small_cargo_ship" : 4000       * 0.5
    ,"big_cargo_ship"   : 12000      
    ,"light_fighter"    : 4000       * 0.5
    ,"heavy_fighter"    : 10000
    ,"cruiser"          : 27000
    ,"battleship"       : 60000 
    ,"battlecruiser"    : 90000
    ,"recycler"         : 20000
    ,"bomber"           : 90000
    ,"destroyer"        : 125000
    ,"deathstar"        : 10000000
  }

class galaxy_generator:
 
  def __init__(self):
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
    
  def compute_total_production(self, buildings, universe_production_multiplier=1):
    if universe_production_multiplier == None:
      universe_production_multiplier = self.config["universe_production_multiplier"]
    total = 0
    for b in ["metal_mine","crystal_mine","deuterium_synthesizer"]: 
      mine_level = buildings[b]
      total = total + 20 * mine_level * 1.1**mine_level
    total = universe_production_multiplier * total
    return math.floor(total)
    
  def compute_planet_juice(self, distance, buildings):
    distance_scaling_factor = self.compute_scaling_factor(distance, mode="exponential")
    seniority_days_factor  = distance_scaling_factor * 365 * 24                        # Up to one year of linear scaling
    seniority_days_factor += math.floor(min(7, max(distance/10*7,0))) * 24             # Most planets have at least one week
    juice = self.compute_total_production(buildings) * seniority_days_factor 
    juice = math.floor(juice)
    return juice
  
  def generate_planet_buildings(self, distance, scaling_factor = None):
    if scaling_factor == None:
      scaling_factor = self.compute_scaling_factor(distance)
    buildings = {}
    buildings["solar_plant"] = 1
    # Mines
    for b in ["metal_mine","crystal_mine","deuterium_synthesizer"]:
      m2 = self.config["level_mines_max"]
      m1 = self.config["level_mines_min"]
      average = self.config["level_mines_min"] + scaling_factor * (math.log(math.exp(m2-m1)-math.exp(m1)))
      blevel = random.gauss(average,2+average/6)
      blevel = max(0,min(50,blevel))
      buildings[b] = math.floor(blevel)
      buildings["solar_plant"] = max(buildings["solar_plant"], buildings[b])
      
    # Storages
    for b in ["metal_storage","crystal_storage","deuterium_tank"]:
      m2 = self.config["level_storage_max"]
      m1 = self.config["level_storage_min"]
      average = self.config["level_storage_min"] + scaling_factor * (math.log(math.exp(m2-m1)-math.exp(m1)))
      blevel = random.gauss(average,average/12)
      blevel = max(0,min(50,blevel))
      buildings[b] = math.floor(blevel)
      
    # Static defenses
    defense_juice = self.compute_planet_juice(distance, buildings) * random.randint(40,100)/100 # Not everyone builds defenses
    defense_buildings = {k: v for k,v in defences.buildings.items() if v < defense_juice }
    total_value_per_item = defense_juice / max(1,len(defense_buildings))
    for k,v in defense_buildings.items():
      quantity = math.floor(total_value_per_item / v * random.randint(50,200)/100)
      if k in ["small_shield_dome","large_shield_dome"]:
        quantity = min(1,quantity)
      if quantity > 0:
        buildings[k] = quantity
      
      
    # Fleets
    fleet_juice = self.compute_planet_juice(distance, buildings)# 
    fleet_ships = {k: v for k,v in defences.fleets.items() if v < fleet_juice }
    total_value_per_item = fleet_juice / max(1,len(defense_buildings))
    for k,v in fleet_ships.items():
      quantity = math.floor(total_value_per_item / v * random.gauss(80,20) / 100)
      if quantity > 0:
        buildings[k] = quantity
    
    
    # Actual juice
    buildings["metal_perhour"]     = 30 * self.config["universe_production_multiplier"] * buildings["metal_mine"]**1.1
    buildings["crystal_perhour"]   = 20 * self.config["universe_production_multiplier"] * buildings["crystal_mine"]**1.1
    buildings["deuterium_perhour"] = 12 * self.config["universe_production_multiplier"] * buildings["deuterium_synthesizer"]**1.1
    
    buildings["metal"]     = buildings["metal_perhour"] * 24*7
    buildings["crystal"]   = buildings["crystal_perhour"] * 24*7
    buildings["deuterium"] = buildings["deuterium_perhour"] * 24*7
    return buildings
    

class planet:

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
    self.generator = galaxy_generator()
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
    ships = {k:v for k,v in self.parameters.items() if k in defences.fleets }
    defenses = {k:v for k,v in self.parameters.items() if k in defences.buildings }
    print()
    if True:
      print("Ships:\n")
      pprint.pprint(ships)
    if True:
      print("Defenses:\n")
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

def retrieve_existing_planets_coordinates():  
  sql = "SELECT galaxy, system, planet FROM _planets"
  cursor.execute(sql)
  existing_planets = cursor.fetchall()
  return existing_planets

def insert_planet(p, existing_planets): 
  if (p.parameters["galaxy"], p.parameters["system"], p.parameters["planet"]) in existing_planets:
    print("Returning to avoid collision at (%d,%d,%d)" % (p.parameters["galaxy"], p.parameters["system"], p.parameters["planet"]))
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

print("This script is highly destructive. Doing nothing. Find this line and uncommment (safety).")
#populate_everything(coordinates_blacklist=retrieve_existing_planets_coordinates())

#cursor.close()                          
cnx.commit()