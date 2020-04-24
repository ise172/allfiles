'''
Created on Apr 17, 2020

@author: Pierr
'''
from Classes.Truck import Truck

class ProductionOrder:
    
    #Initializes the variables for the order
    def __init__(self,id,prodProcess,finalLocation,lineLocations,trucks,vehicles,graph):
        self.ID = id
        self.totalTime = 0 
        self.trucks = trucks
        self.graph = graph
        self.vehicles = vehicles #The list of truck objects being used for re-stocking the production lines to be used
        self.prodProcess = prodProcess
        self.finalLocation = finalLocation
        self.transit = [0,-1,0] # represents the movement between prod. lines and the final location (third value will be the truck object that is being used)
        self.finished = False
        self.readyForFinalLocation = False
        self.currentProcess = self.prodProcess[0]
        self.lines = lineLocations
        self.shipments = []
        for line in lineLocations:
            temp = [line.shipmentOnWay[0],line.shipmentOnWay[1]]
            self.shipments.append(temp) 
        self.currentProcessProgress = [0,self.currentProcess['processingTime']]
    
    
    # Prints the order information
    def __str__(self):
        return "\nOrder "+str(self.ID)+": " + str(self.prodProcess)+ "\n    Current process: "+ str(self.currentProcess)+" is " +str(self.currentProcessProgress[0])+" out of "+str(self.currentProcessProgress[1])+" minutes complete at the production line located at node "+str(self.lines[0].location)+" Shipment on Way?: "+str(self.shipments[0])+" Transit: "+str(self.transit)
    
    # Updates the order
    def update_order(self):
        self.totalTime = self.totalTime + 1 #tracks the total time for the order
        if not self.readyForFinalLocation:
            #Check if the shipments of material have arrived and update accordingly
            self.update_shipments()
            if self.shipments[0][0] == False: #this means that we are not waiting for a shipment of material to arrive so we can proceed with the process
                if self.transit[0] < self.transit[1]: 
                    self.transit[0] = self.transit[0]+1 #if the order is in transit between production lines, increment this counter and return
                    if self.transit[0] == self.transit[1]:
                        self.transit[2].free() #free's the truck if the transit is complete
                    return
                if self.currentProcessProgress[0] == self.currentProcessProgress[1]: #This indicates that the current process is complete, so we can go to the next process (or final location if this was the last process)
                    if len(self.prodProcess) <= 1: #means that we are ready for the final transit
                        self.update_transit(self.lines[0].location,self.finalLocation)
                        self.readyForFinalLocation = True
                        return
                    self.update_transit(self.lines[0].location,self.lines[1].location)
                    self.next_process()
                    return
                #update inventory of line
                if self.currentProcessProgress[0] == 0:
                    self.lines[0].inventory[self.currentProcess['resourceNeeded']] = self.lines[0].inventory[self.currentProcess['resourceNeeded']] - self.currentProcess['materialNeeded[tons]']
                #update current process progress
                temp = self.currentProcessProgress[0] + 1
                self.currentProcessProgress= [temp,self.currentProcess['processingTime']]
        else: #measures progress along the final transit and marks the order as finished once we reach it
            if self.transit[0] < self.transit[1]:
                    self.transit[0] = self.transit[0]+1
            if self.transit[0] == self.transit[1]:
                self.transit[2].free()
                self.finished = True
            return    
    
    #Determines the best truck to more the WiP/Finished good from a given start node to an end node
    def update_transit(self,start_node,end_node):
        #Find closest truck to start node and gives it the path, then adds the path from start to end nodes. Updates the transit counter
        distance,index=1000,0
        for truck in self.trucks:
            if truck.occupied:
                continue
            temp = self.graph.floyd_warshall(truck.location[1][0],start_node)
            length = self.graph.floyd_warshall_length(temp)
            if length <distance:
                distance = length
                path1 = temp
                index = truck.ID
        if not self.trucks[index].occupied:
            self.trucks[index].path = path1
            self.trucks[index].occupied = True
        else:
            print "No trucks available for the transit"
            return
        path2 = self.graph.floyd_warshall(start_node,end_node)
        path2.pop(0)
        while len(path2) > 0:
            self.trucks[index].path.append(path2.pop(0))
        pathLength = self.graph.floyd_warshall_length(self.trucks[index].path)
        self.transit = [0,pathLength,self.trucks[index]]
    
    # Checks to see if there is a shipment of goods coming, and if so, updates the progress of the truck
    def update_shipments(self):
        for shipment in self.shipments:
            if shipment[0] == True:
                if shipment[1] == 1:
                    shipment[0] = False
                    shipment[1] = 0
                    if len(self.vehicles) > 0:
                        self.vehicles[0].free()
                else:
                    shipment[1] = shipment[1] - 1    
    
    # Updates the variables of the order to prepare for the next process in the production 
    def next_process(self):
        self.prodProcess.pop(0)
        self.currentProcess = self.prodProcess[0]
        if len(self.vehicles) > 1:
            self.vehicles.pop(0)
        self.lines.pop(0)
        self.shipments.pop(0)
        self.currentProcessProgress = [0,self.currentProcess['processingTime']]
        
                    
                    
                    