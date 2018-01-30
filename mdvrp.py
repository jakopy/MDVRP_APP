from gurobi_vrp import *
from gurobipy import *
from distancematrixmaker import *
from depot_match import depot_matcher
import types

class mdvrp_solve():
    def __init__(self, siteNames,dist,depot_list,demand,capacity,match_type,depot_capacity_list):
        self.siteNames = siteNames
        self.dist = dist
        self.depot_list = depot_list
        self.demand = demand
        self.capacity = capacity
        self.match_type = match_type
        self.depot_capacity_list = depot_capacity_list

    def run(self):
        siteNames = self.siteNames
        dist = self.dist
        depot_list = self.depot_list
        demand = self.demand
        capacity = self.capacity
        match_type = self.match_type
        depot_capacity_list = self.depot_capacity_list

        #Depot Match Algo
        depots_matched = depot_matcher(siteNames,depot_list,dist).run(match_type,depot_capacity_list)

        #Solve Sub VRP Problems
        master_solution = {}
        sub_prob_count = 0
        for depot in depots_matched:
            if depots_matched[depot] != None:
                nodes = depots_matched[depot]
                sub_prob = [depot] + nodes
                sub_dist = []
                sub_siteNames = []
                sub_demand = []
                counter = -1
                for i in sub_prob:
                    sub_dist.append([])
                    sub_siteNames.append(siteNames[i])
                    sub_demand.append(demand[i])
                    counter +=1
                    for j in sub_prob:
                        sub_dist[counter].append(dist[i][j])
                sub_sites = range(len(sub_siteNames))
                sub_clients = sub_sites[1:]

                sub_prob_count+=1
                #execute vrp
                vrpsol = VRPsolve(sub_dist,sub_demand,capacity,sub_sites,sub_clients,sub_siteNames).run()
                master_solution[depot] = vrpsol
            else:
                master_solution[depot] = None

        routify = []
        for depot in master_solution:
            if master_solution[depot] != None:
                vrp_sol = master_solution[depot]
                for bus in vrp_sol:
                    routes = vrp_sol[bus][2]
                    routify.append(routes)
            else:
                depot_name = siteNames[depot]
                routify.append(depot_name)
        return routify, master_solution

class geocoder():
    def __init__(self,coords,siteNames,route):
        self.coords = coords
        self.siteNames = siteNames
        self.route = route
    def run(self):
        siteNames = self.siteNames
        coords = self.coords
        routify = self.route
        lat_lon = coords.split("|")

        addr_to_latlng = {}
        counter = 0
        for address in siteNames:
            addr_to_latlng[address] = "("+lat_lon[counter]+")"
            counter += 1

        master_routes = []
        for route in routify:
            if isinstance(route, types.StringTypes) == False:
                builder = []
                for loc in route:
                    builder.append(addr_to_latlng[loc])
                master_routes.append(builder)
            else:
                master_routes.append([addr_to_latlng[route]])
        return master_routes


if __name__ == "__main__":

    #PULL IN DATA WITH DISTANCE MATRIX MAKER
    coords = "38.888665,-77.076817|38.811768,-77.054556|38.731186,-77.056399|38.891624,-77.101873|38.807791,-77.063039|38.81696,-77.042368|38.835419,-77.053051|38.800536,-77.045838|38.834099,-77.092047|38.820301,-77.052691"
##    siteNames, dist = matrixmaker(coords).matrix()

    siteNames = ['1220 N Pierce St, Arlington, VA 22209, USA', '541 Colecroft Ct, Alexandria, VA 22314, USA', '8320 Fort Hunt Rd, Fort Hunt, VA 22308, USA', 'Custis Memorial Pkwy, Arlington, VA 22201, USA', '2032-2064 King St, Alexandria, VA 22314, USA', '1101-1105 N Pitt St, Alexandria, VA 22314, USA', '236-240 Evans Ln, Alexandria, VA 22305, USA', '420-426 S Pitt St, Alexandria, VA 22314, USA', '4612 34th St S, Arlington, VA 22206, USA', '1511 Leslie Ave, Alexandria, VA 22301, USA']
    dist = [[0, 12677, 21389, 6104, 12655, 11658, 7991, 13079, 9414, 12080], [12935, 0, 10370, 19937, 1409, 1919, 3626, 2053, 5085, 1805], [21572, 10367, 0, 28573, 11651, 10551, 12838, 8704, 15698, 11848], [4861, 15618, 24330, 0, 15481, 14598, 10937, 16020, 12241, 12697], [11650, 1486, 10361, 14571, 0, 3206, 3772, 2056, 4181, 2540], [11413, 1919, 10558, 18414, 2936, 0, 2984, 1851, 14284, 1994], [8107, 3473, 12872, 14139, 3821, 3232, 0, 4566, 4589, 2067], [13261, 2056, 8702, 20262, 2349, 1851, 4529, 0, 6544, 3539], [8494, 5194, 14501, 11415, 4139, 13980, 4899, 6195, 0, 4681], [10232, 1765, 11734, 16264, 2352, 2907, 2289, 3428, 4686, 0]]
    demand = [ 10,10, 12, 16, 14, 12, 10, 17, 18, 12, 8]
    capacity = 30

    #optimally split on nodes closest to depot
    match_type = ""
    depot_capacity_list = None

    #pick first 2 to be the depot_list
    depot_list = siteNames[0:2]

    #Build out a constant demand
##    const_demand = 12
##    demand = []
##    for i in siteNames:
##        if i not in depot_list:
##            demand.append(const_demand)
##        else:
##            demand.append(0)

    routify,master_sol = mdvrp_solve(siteNames,dist,depot_list,demand,capacity,match_type,depot_capacity_list).run()

    #change route to coords
    master_routes = geocoder(coords,siteNames,routify).run()
    for i in master_routes:
        print i
