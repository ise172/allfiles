'''
Created on Mar 6, 2020

@authors: Pierre, Andrew, Anna, Owen
'''
#import math and pygame 
import pygame
import math


class Animation():
    #Initializes the animation and variables needed
    def __init__(self, graph):
        self.Edges = graph.Edges
        self.Verticies = graph.Verticies
        self.dimx = 1500
        self.dimy = 1050
        self.font1  = pygame.font.SysFont('Comic Sans MS', 30)
        self.font2  = pygame.font.SysFont('Comic Sans MS', 12)
        self.time = 0
    
    #Creates the pygame window to display the animation
    def initialize_animation(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.dimx,self.dimy))
        pygame.display.set_caption("S-LaBuT")
        self.background = self.screen.convert()
        self.clock = pygame.time.Clock()
    
    #Updates the animation window by displaying the time and drawing the graphs and trucks (This function is called every minute of the simulation)
    def update_animation(self,trucks): 
        self.screen.fill((255,255,255))
        Animation.draw_time(self)
        Animation.draw_edges(self)
        Animation.draw_verticies(self)
        Animation.display_truck_locations(self, trucks)
        pygame.display.flip()
        pygame.time.delay(10)
    
    #Displays the time in the top left corner of the window
    def draw_time(self):
        text = self.font1.render("Time: %02d:%02d"%(self.time/60, self.time%60), True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = 100
        textrect.centery = 30
        self.screen.blit(text, textrect)
    
    #Loops through the list of vertices and draws a blue circle with the number of the vertex in the animation window
    def draw_verticies(self):
        for vertex in self.Verticies:
            center = (vertex[1],vertex[2])
            pygame.draw.circle(self.screen,(0,0,200),center,12)
            text = self.font2.render("%d"%(vertex[0]), True, (255, 255, 255))
            textrect = text.get_rect()
            textrect.centerx = center[0]
            textrect.centery = center[1]
            self.screen.blit(text, textrect)
    
    #Loops through the list of edges and draws red lines representing the edges. If the edge is curved, loop through each of the points on the curve and draw small line segments.
    def draw_edges(self):
        for edge in self.Edges:
            if len(edge[3]) > 2:
                #CURVE
                n = len(edge[3])
                count = 0
                while count < n-1:
                    start = (edge[3][count][0],edge[3][count][1])
                    end =  (edge[3][count+1][0],edge[3][count+1][1])
                    pygame.draw.line(self.screen,(200,0,0), start, end,2)
                    count += 1
            else:
                #STRAIGHT LINE
                start = (edge[3][0][0],edge[3][0][1])
                end = (edge[3][1][0],edge[3][1][1])
                pygame.draw.line(self.screen,(200,0,0), start, end,2)
    
    #loops through the list of truck objects and displays the location of each one
    def display_truck_locations(self,trucks):
        for truck in trucks:
            coordinates = truck.graph.get_coordinates(truck.location[1][0]) #coordinates of the start node
            step = float(truck.location[1][2])/float(truck.location[1][3]) #how far along the path from node A to node B as a decimal
            #CURVE
            if len(truck.edge[3]) > 2:
                length,n,count = 0,len(truck.edge[3]),0
                while count < n-1:#This while loop gets the total length of the curved path
                    length = length + math.sqrt((truck.edge[3][count+1][0]-truck.edge[3][count][0])**2 + (truck.edge[3][count+1][1] - truck.edge[3][count][1])**2) 
                    count = count +1
                move = step*length #determines how far we have to move from the start node
                count = 0
                while count < n-1: #This for loop determines which of the smaller segments we are on and then gets the new location
                    current_segment = math.sqrt((truck.edge[3][count+1][0]-truck.edge[3][count][0])**2 + (truck.edge[3][count+1][1] - truck.edge[3][count][1])**2)
                    if move > current_segment:
                        move = move - current_segment
                        count = count + 1
                        continue
                    x2,y2 = truck.edge[3][count+1][0],truck.edge[3][count+1][1]
                    x1,y1 = truck.edge[3][count][0], truck.edge[3][count][1]
                    location = (int(x1 + float(move/current_segment)*(x2-x1)),int(y1 + float(move/current_segment)*(y2-y1)))
                    break
                if truck.location[1][2] == truck.location[1][3]: #ensures that the location of the dot is at the node when we arrive at the vertex (offsets the sounding errors)
                    location = truck.graph.get_coordinates(truck.location[1][1])
            #STRAIGHT LINE
            else:
                x = coordinates[0] + step*truck.delta[0]
                y = coordinates[1] + step*truck.delta[1]
                location = (int(x),int(y))
            pygame.draw.circle(self.screen, (0,200,0),location,5) #Draw a green dot to represent the truck
        
        
            
            
            
            
            
            
            