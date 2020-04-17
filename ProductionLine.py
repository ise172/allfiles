'''
Created on Apr 17, 2020

@author: Pierre
'''

class ProductionLine:
    def __init__(self,location,line,capacity):
        self.location = location
        self.type = line
        self.capacity = capacity
        self.inventory = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0, 'H': 0, 'Total': 0}
        self.busy = False
        self.currentJobs = 0
        self.shipmentOnWay = False

    
    def get_resources(self,resource,amountNeeded,trucks,graph,warehouses):
        options = []
        for w in warehouses:
            if w.type == resource:
                options.append(w)
        distance,index = 1000,0
        for t in trucks:
            if t.capacity < amountNeeded or t.occupied:
                continue
            for warehouse in options:
                temp = graph.floyd_warshall(t.location[1][0],warehouse.location)
                length = len(temp)
                if length < distance:
                    distance = length
                    path1 = temp
                    index = t.ID
                    
        if not trucks[index].occupied:
            trucks[index].path = path1
            trucks[index].occupied = True
            shipment = trucks[index].capacity
            trucks[index].capacity = 0
        else:
            print "No available trucks"
            return
        path2 = graph.floyd_warshall(path1[len(path1)-1],self.location)
        path2.pop(0)
        while len(path2) > 0:
            trucks[index].path.append(path2.pop(0))
        print "path of truck ", index, ": ", trucks[index].path 
        
        self.inventory[resource] = self.inventory[resource] + shipment
        self.update_total_inventory()
        self.shipmentOnWay = True
        self.currentJobs = self.currentJobs + 1

    
    def update_total_inventory(self):
        total = 0
        for key in self.inventory:
            total = total + self.inventory[key]
        self.inventory['Total'] = total




                
        