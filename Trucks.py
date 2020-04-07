'''
Created on Mar 27, 2020

@author: Pierre
'''
from Classes.Graph import Graph

class Trucks:
    
    def __init__(self, path, graph):
        self.graph = graph
        self.vertex = True
        self.path = path
        self.cost = 0
        self.location = (self.vertex,(0,0,0, self.cost))
        self.delta = (0,0)

        
    def update_truck_location(self):
        #If the truck has reached its final destination, skip this method
        if len(self.path) <= 1:
            return
        #Check if truck is at a node. If it is, the new destination is the next node in the path and we are on a new trip so the cost and deltaX/Y must be updated
        if self.location[0] == True:
            self.cost = self.graph.get_cost(self.path[0],self.path[1])
            self.location = (False,(self.path[0],self.path[1],0,self.cost))
            current = self.graph.get_coordinates(self.path[0])
            destination = self.graph.get_coordinates(self.path[1])
            self.delta = (destination[0]-current[0], destination[1]-current[1])
        
        temp1 = self.location[1]
        temp2 = temp1[2]
        temp2 = temp2 + 1       
        self.location = (False, (self.path[0],self.path[1],temp2,self.cost))
        if self.location[1][2] == self.location[1][3]:
            self.location = (True,(self.path[0],self.path[1],temp2,self.cost))
            self.path.pop(0)
          