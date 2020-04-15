'''
Created on Mar 27, 2020

@author: Pierre
'''

class Trucks:
    #Initializes the truck object with its path, graph and location
    def __init__(self, location, graph, capacity):
        self.graph = graph
        self.vertex = True
        self.path = [location]
        self.cost = 1000
        self.location = (self.vertex,(location,location,0, self.cost)) #(Vertex/Edge, (from node u, to node v, traveled x minutes, out of cost c))
        self.edge = [0, 0, 0, [(0, 0), (0, 0)], 'B']
        self.capacity = capacity
        self.occupied = False

    #Updates the truck locations
    def update_truck_location(self):
        #If the truck has reached its final destination, skip this method (ie return now)
        if len(self.path) <= 1:
            return
        #Check if truck is at a node. If it is, we must progress to a new edge (u,v) so the cost and deltaX/Y must be updated to correspond to this edge
        if self.location[0] == True:
            self.cost = self.graph.get_cost(self.path[0],self.path[1]) #updates the cost of this edge
            self.location = (False,(self.path[0],self.path[1],0,self.cost)) #updates the location of the truck
            self.edge = self.graph.get_edge(self.path[0],self.path[1])
        #Increments the distance along the path by 1 minute
        temp = self.location[1][2] + 1    
        self.location = (False, (self.path[0],self.path[1],temp,self.cost))
        #If the truck is at a node, the self.vertex boolean becomes true and we pop the first element off the path so it represents the remaining path to be traveled
        if self.location[1][2] == self.location[1][3]: 
            self.location = (True,(self.path[0],self.path[1],temp,self.cost))
            self.path.pop(0)