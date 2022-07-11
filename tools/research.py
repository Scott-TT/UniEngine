import math
import economy_config

class Research:
    def __init__(self, metal, crystal, deut, dependencies=None):
        self.metal = metal
        self.crystal = crystal
        self.deut = deut
        if dependencies==None:
            self.dependencies=[]
        else:
            self.dependencies = dependencies

    def get_total_cost(self, level):
        cost = {}
        for r in ["metal","crystal","deut"]:
            total_cost = math.floor(getattr(self,r) * (math.pow(2,level-1)))
            for dependency in self.dependencies:
                for dep_tech, dep_level in dependency.items():
                    total_cost += (all_techs[dep_tech].get_total_cost(dep_level))[r]
            cost[r] = total_cost
        return cost

    def get_simplified_cost(self, level):
        cost = self.get_total_cost(level)
        return cost["metal"]*economy_config.metal_cost_ratio + cost["crystal"]*economy_config.crystal_cost_ratio + cost["deut"]*economy_config.deut_cost_ratio


all_techs = {
     "espionage" : Research(200, 1000, 200)
    ,"computer" : Research(400,600,0)
    ,"weapons" : Research(800,200,0)
    ,"shielding" : Research(200,600,0, dependencies=[{"espionage":3}])
    ,"armour" : Research(1000,0,0)
    ,"energy" : Research(0,800,400)
    ,"hyperspace" : Research(0,4000,2000, dependencies=[{"energy":5},{"shielding":5}])
    ,"combustion_drive" : Research(400,0,600, dependencies=[{"energy":1}])
    ,"impulse_drive" : Research(2000,4000,600, dependencies=[{"energy":1}])
    ,"hyperspace_drive" : Research(10000,20000,6000, dependencies=[{"hyperspace":3}])
    ,"laser" : Research(200,100,0, dependencies=[{"energy":2}])
    ,"ion" : Research(1000,300,0, dependencies=[{"laser":5},{"energy":4}])
    ,"plasma" : Research(2000,4000,0, dependencies=[{"laser":10},{"energy":8},{"ion":5}])
    ,"IRN" : Research(240000,400000,160000, dependencies=[{"computer":8},{"hyperspace":8}])
    ,"astrophysic" : Research(4000,8000,4000)
}
