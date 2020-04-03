'''
Created on Mar 27, 2020

@author: Pierre
'''

class Trucks:
    
    def __init__(self,location, path):
        self.location = location
        self.path = path
        #Example from takac:
        # t.loc = (E, (1,2,3,5))
        #or 
        # t.loc = (V,17)
        
        
    def update_truck_location(self):
        #Check is truck is at a node
        x1 = self.location[0]
        y1 = self.location[1]
        x2 = #next node in path
        y2 = 
        deltaX = x2-x1
        deltaY = y2-y1
        tripLength = #cost of the edge
        newx = x1 + deltaX/tripLength
        newy = y1 + deltaY/tripLength
        self.location = (newx,newy)
        

    '''
    def __init__(self):
        self.number_of_trucks = 0
        self.locations = {} #list of truck locations 
        self.final_destinations = {}
        self.next_destinations = {}
        self.paths = {}
    
    def add_truck(self,truck_ID):
        self.locations[truck_ID] = (0,0)
        self.number_of_trucks += 1
    
    def initialize_coordinates(self,truck_ID,start_coordinates,end_coordinates,path):
        self.locations[truck_ID] = start_coordinates
        self.final_destinations[truck_ID] = end_coordinates
        self.paths[truck_ID] = path
        self.next_destinations[truck_ID] = self.paths[truck_ID].pop(1)
        
    def set_next_destination(self):
        for i,truck in enumerate(self.locations):
            if len(self.paths[i]) > 1:
                self.next_destinations[i] = self.paths[i].pop(1)
            #print "Next destination for truck ", i, ": ", self.next_destinations[i]
    
       
    def update_truck_locations(self):
        print "locations: ", self.locations
        for i,truck in enumerate(self.locations):
            print "Location of ", i, "  before: ", self.locations[i]
            print "Destination: ", self.next_destinations[i]
            x1, y1 = self.locations[i][0], self.locations[i][1]
            x2, y2 = self.next_destinations[i][0], self.next_destinations[i][1]
            if not ((x2-5)<=x1<=(x2+5)and(y2-5)<=y1<=(y2+5)):
                slope, xnew, ynew = 0.0, 0.0, 0.0
                if x2 == x1:
                    x1 += 1
                slope = (float(y2)-float(y1))/(float(x2)-float(x1))
                if x1 < x2:
                    xnew = float(x1) + 2.0
                else:
                    xnew = float(x1) - 2.0
                ynew = float(y1) + slope*(xnew-float(x1))
                #xnew = x1 + (x2-x1)/2
                #ynew = y1 + (y2-y1)/2
                self.locations[i] = (int(xnew),int(ynew))
                print "Location of ", i, " after: ", self.locations[i]
            else:
                Trucks.set_next_destination(self)
    
    '''           
          
    def update_truck_locations(self):
        print "locations: ", self.locations
        print "next destinations: ", self.next_destinations
        for i,truck in enumerate(self.locations):
            #print "Location of ", i, "  before: ", self.locations[i]
            #print "Destination: ", self.next_destinations[i]
            x1, y1 = self.locations[i][0], self.locations[i][1]
            x2, y2 = self.next_destinations[i][0], self.next_destinations[i][1]
            if not ((x2-5)<=x1<=(x2+5)and(y2-5)<=y1<=(y2+5)):
                if x1 < x2:
                    xnew = x1 + 5
                if x1 >= x2: 
                    xnew = x1 - 5
                if y1 < y2:
                    ynew = y1 + 5
                if y1 >=y2:
                    ynew = y1 - 5
                self.locations[i] = (xnew,ynew)
                #print "Location of ", i, " after: ", self.locations[i]
            else:
                Trucks.set_next_destination(self)            
                
    '''           
