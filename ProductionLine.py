'''
Created on Apr 17, 2020

@author: Pierre
'''

class ProductionLine:
    #initializes variables of the production line
    def __init__(self,location,line,capacity):
        self.location = location
        self.type = line
        self.capacity = capacity
        self.inventory = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'Total': 0}
        self.busy = False
        self.currentJobs = 0
        self.shipmentOnWay = [False,0]
        self.holdingCost = 0

    #Finds the closest truck to a warehouse of the correct type and sends it on a path from its current location, to the warehouse to pick up resources, to the current prod line.
    def get_resources(self,resource,amountNeeded,trucks,graph,warehouses,time):
        options = []
        for w in warehouses: #compiles a list of warehouses that are the correct type
            if w.type == resource:
                options.append(w)
        distance,index = 1000,0
        for t in trucks: # for each truck, if it is not busy, finds the shortest path to each warehouse and keeps track of the index of the truck with the shortest path 
            if t.capacity[0] < amountNeeded or t.occupied:
                continue
            for warehouse in options:
                temp = graph.floyd_warshall(t.location[1][0],warehouse.location)
                length = graph.floyd_warshall_length(temp)
                if length < distance:
                    distance = length
                    path1 = temp
                    index = t.ID
        # adds the path to the truck and updates the shipment amount 
        if not trucks[index].occupied:
            trucks[index].path = path1
            trucks[index].occupied = True
            shipment = trucks[index].capacity[0]
            trucks[index].capacity[0] = 0
        else:
            print "No available trucks to get resources"
            return
        #Finds the shortest path from the chosen warehouse to the current prod line and adds those nodes to the path of the truck 
        path2 = graph.floyd_warshall(path1[len(path1)-1],self.location) 
        path2.pop(0)
        while len(path2) > 0:
            trucks[index].path.append(path2.pop(0))
        print "path of truck ", index, ": ", trucks[index].path 
        pathLength = graph.floyd_warshall_length(trucks[index].path)
        #Updates the inventory of the current prodLine, and notes that a shipment is on the way
        self.inventory[resource] = self.inventory[resource] + shipment
        self.update_total_inventory()
        self.shipmentOnWay = [True,pathLength+1]
        self.currentJobs = self.currentJobs + time
        return trucks[index]

    # Updates the total inventory by summing all of the different types of matrial
    def update_total_inventory(self):
        total = 0
        for key in self.inventory:
            total = total + self.inventory[key]
        self.inventory['Total'] = total
    
    #Updates the holding cost 
    def update_holding_cost(self):
        self.holdingCost = self.holdingCost + 5 * self.inventory['Total']




                
        