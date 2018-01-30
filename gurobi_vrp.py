from gurobipy import *

class VRPsolve():
    def __init__(self,dist,demand,capacity,sites,clients,siteNames):
        self.dist = dist
        self.demand = demand
        self.capacity = capacity
        self.sites = sites
        self.clients = clients
        self.siteNames = siteNames
    def run(self):
        dist = self.dist
        demand = self.demand
        capacity = self.capacity
        sites = self.sites
        clients = self.clients
        siteNames = self.siteNames
        model = Model('Diesel Fuel Delivery')
        x = {}
        arcs = []
        routes = {}
        for i in sites:
            for j in sites:
                x[i,j] = model.addVar(vtype=GRB.BINARY,name="routes")

                arcs.append((i,j))

        u = {}
        quant = {}
        us = []
        for i in clients:
            u[i] = model.addVar(lb=demand[i], ub=capacity)
            us.append(i)
            quant[i] = demand[i]

        model.update()

        model.setObjective(quicksum(dist[i][j]*x[i,j] for i in sites for j in sites if i != j),GRB.MINIMIZE)

        thesum = 0
        for j in clients:
            model.addConstr(quicksum( x[i,j] for i in sites if i != j ) == 1)

        for i in clients:
            model.addConstr(quicksum( x[i,j] for j in sites if i != j ) == 1)

        for i in clients:
            model.addConstr(u[i] <= capacity + (demand[i] - capacity)*x[0,i])
##            model.addConstr(u[i] == capacity + (demand[i] - capacity)*x[0,i])

        for i in clients:
            for j in clients:
                if i != j:
                    model.addConstr(u[i] - u[j] + capacity*x[i,j] <= capacity - quant[j])

        model.setParam('OutputFlag',False)
        model.optimize()
        # Print Solution
        if model.status == GRB.Status.OPTIMAL:
            solution = model.getAttr('x')
            arcsol = []
            for i in range(0,len(solution),1):
                if solution[i] == 1:
                    print arcs[i] , " : ", solution[i]
                    arcsol.append(arcs[i])

        #COUNT NUMBER OF ROUTES
        counter = 0
        counter_list = []
        for arc in arcsol:
            if arc[0] == 0:
                counter_list.append(counter)
                counter += 1

        #ROUTE FINDER
        ROUTE_LIST = []
        for c in counter_list:
            Single_Route = []
            counter = 0
            for arc in arcsol:
                if arc[0] == 0:
                    counter += 1
                    if counter > c:
                        if arc[0] not in Single_Route:
                            Single_Route.append(arc[0])
                            Single_Route.append(arc[1])
                if len(Single_Route) > 0:
                    next_one = Single_Route[len(Single_Route)-1]
                    for arc in arcsol:
                        if next_one == 0:
                            break
                        if arc[0] == next_one:
                            Single_Route.append(arc[1])
            ROUTE_LIST.append(Single_Route)

        #BUILD RESULTS SET
        result_set = {}
        bus_number = 1
        total_picked_up = 0
        distance_traveled = 0
        for route in ROUTE_LIST:
            i = 0
            single_route = []
            for j in range(1,len(route)-1,1):
                single_route.append(siteNames[route[i]])
                single_route.append(siteNames[route[j]])
                total_picked_up+=demand[route[j]]
                distance_traveled+=dist[route[i]][route[j]]
                arc = route[i],route[j]
                #print arc
                i+=1
            distance_traveled+=dist[route[len(route)-2]][route[len(route)-1]]
            single_route.append(siteNames[route[len(route)-2]])
            single_route.append(siteNames[route[len(route)-1]])
            arc = route[len(route)-2],route[len(route)-1]
            #print arc
            result_set["Bus " + str(bus_number)] = [distance_traveled,total_picked_up,single_route]
            bus_number += 1
        print result_set
        return result_set

if __name__ == "__main__":
    siteNames = ["Reno", "South Lake Tahoe", "Carson City", "Garnerville",
                  "Fernerly", "Tahoe City", "Incline Village", "Truckee"]
    sites = range(len(siteNames))
    clients = sites[1:]
    #print "THE LENGTH OF CLIENTS: " + str(len(clients))
    demand = [ 0,1000, 1200, 1600, 1400, 1200, 1000, 1700]
    demandsum = 0
    for i in demand:
        demandsum += i
    #print "THE DEMAND SUM IS: " + str(demandsum)
    dist = [[0, 59.3, 31.6, 47.8, 34.2, 47.1, 36.1, 31.9],
            [62.2, 0, 27.9, 21.0, 77.5, 30.0, 27.1, 44.7],
            [32.2, 27.7, 0, 16.2, 50.0, 39.4, 24.9, 42.6],
            [50.7, 21.0, 16.4, 0, 66.1, 49.7, 35.2, 52.9],
            [34.4, 77.4, 49.6, 65.9, 0, 80.8, 67.1, 65.5],
            [46.9, 30.1, 39.6, 49.7, 80.5, 0, 14.4, 15.0],
            [36.9, 27.1, 25.2, 35.2, 67.1, 14.4, 0, 17.6],
            [31.9, 44.7, 62.8, 52.8, 65.6, 15.0, 17.6, 0]]


    capacity = 5000

    #execute the function
    vrpsolve = VRPsolve(dist,demand,capacity,sites,clients,siteNames)
    vrpsol = vrpsolve.run()

    #parse the sol
    for bus in vrpsol:
        distance = vrpsol[bus][0]
        demand = vrpsol[bus][1]
        routelist = vrpsol[bus][2]
        print bus
        print distance
        print demand
        print routelist
