import math

import economy_config
import research

class PlanetItem:
    def __init__(self, metal, crystal, deut, key=None, maximum_quantity=None, tech_required=None, buildings_required=None):
        self.metal = metal
        self.crystal = crystal
        self.deut = deut
        self.key = key
        self.maximum_quantity = maximum_quantity
        self.juice = math.floor(metal*economy_config.metal_cost_ratio + crystal*economy_config.crystal_cost_ratio + deut*economy_config.deut_cost_ratio)
        if tech_required == None:
            self.tech_required = {}
        else:
            self.tech_required = tech_required
        if buildings_required == None:
            self.buildings_required = {}
        else:
            self.buildings_required = buildings_required

    # Note: tech overlaps are counted twice(or more). Not worth the bother currently.
    def simplified_tech_cost(self):
        cost = 0
        for tech_type, tech_level in self.tech_required.items():
            cost += research.all_techs[tech_type].get_simplified_cost(level=tech_level, levelup_only=False, include_dependencies=True)
        return math.floor(cost)

    def simplified_cost(self):
        return self.juice

    def total_cost(self):
        return self.metal + self.crystal + self.deut

# Init all buildings
buildings={}
for item in [
     PlanetItem(key="rocket_launcher"      , metal=2000  ,crystal=0     ,deut=0     ,maximum_quantity=None)
    ,PlanetItem(key="light_laser"          , metal=1500  ,crystal=500   ,deut=0     ,maximum_quantity=None)
    ,PlanetItem(key="heavy_laser"          , metal=6000  ,crystal=2000  ,deut=0     ,maximum_quantity=None)     
    ,PlanetItem(key="gauss_cannon"         , metal=20000 ,crystal=15000 ,deut=2000  ,maximum_quantity=None)
    ,PlanetItem(key="ion_cannon"           , metal=3000  ,crystal=5000  ,deut=0     ,maximum_quantity=None)   
    ,PlanetItem(key="plasma_turret"        , metal=50000 ,crystal=50000 ,deut=30000 ,maximum_quantity=None)
    ,PlanetItem(key="small_shield_dome"    , metal=10000 ,crystal=10000 ,deut=0     ,maximum_quantity=1)
    ,PlanetItem(key="large_shield_dome"    , metal=50000 ,crystal=50000 ,deut=0     ,maximum_quantity=1)
    ,PlanetItem(key="antiballistic_missile", metal=12500 ,crystal=2500  ,deut=10000 ,maximum_quantity=150) 
    ]:
    buildings[item.key] = item

# Init all fleets
fleets = {}
for item in [
     PlanetItem(key="small_cargo_ship", metal=2000    ,crystal=2000    ,deut=0       )
    ,PlanetItem(key="big_cargo_ship", metal=6000    ,crystal=6000    ,deut=0       )      
    ,PlanetItem(key="light_fighter", metal=3000    ,crystal=1000    ,deut=0       )
    ,PlanetItem(key="heavy_fighter", metal=6000    ,crystal=4000    ,deut=0       )
    ,PlanetItem(key="cruiser", metal=20000   ,crystal=7000    ,deut=2000    )
    ,PlanetItem(key="battleship", metal=45000   ,crystal=15000   ,deut=0       ) 
    ,PlanetItem(key="battlecruiser", metal=30000   ,crystal=40000   ,deut=15000   )
    ,PlanetItem(key="recycler", metal=10000   ,crystal=6000    ,deut=2000    )
    ,PlanetItem(key="bomber", metal=50000   ,crystal=25000   ,deut=15000   )
    ,PlanetItem(key="destroyer", metal=60000   ,crystal=50000   ,deut=15000   )
    ,PlanetItem(key="deathstar", metal=5000000 ,crystal=4000000 ,deut=1000000 )
    ]:
    fleets[item.key] = item

# Add dependencies (delayed for clarity)
fleets["small_cargo_ship"].tech_required = {"combustion_drive":2}
fleets["big_cargo_ship"].tech_required = {"combustion_drive":6}
fleets["light_fighter"].tech_required = {"combustion_drive":1}
fleets["heavy_fighter"].tech_required = {"armour":2,"impulse_drive":2}
fleets["cruiser"].tech_required = {"impulse_drive":4,"ion":2}
fleets["battleship"].tech_required = {"hyperspace_drive":4}
fleets["battlecruiser"].tech_required = {"hyperspace":5,"laser":12,"hyperspace_drive":5}
fleets["recycler"].tech_required = {"combustion_drive":6,"shielding":2}
fleets["bomber"].tech_required = {"impulse_drive":6,"plasma":5}
fleets["destroyer"].tech_required = {"hyperspace_drive":6,"hyperspace":5}
fleets["deathstar"].tech_required = {"hyperspace_drive":7,"hyperspace":6}  # Graviton skipped
