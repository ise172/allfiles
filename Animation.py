'''
Created on Mar 6, 2020

@author: Pierre, Andrew, Anna, Owen
'''

import pygame
import math


class Animation():
    def __init__(self, graph):
        self.Edges = graph.Edges
        self.Verticies = graph.Verticies
        self.dimx = 1500
        self.dimy = 1050
        self.font1  = pygame.font.SysFont('Comic Sans MS', 30)
        self.font2  = pygame.font.SysFont('Comic Sans MS', 12)
        self.time = 0
    
    def initialize_animation(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.dimx,self.dimy))
        pygame.display.set_caption("Graph")
        self.background = self.screen.convert()
        self.clock = pygame.time.Clock()
    
    def update_animation(self,trucks): 
        self.screen.fill((255,255,255))
        Animation.draw_time(self)
        Animation.draw_edges(self)
        Animation.draw_verticies(self)
        Animation.display_truck_locations(self, trucks)
        pygame.display.flip()
        pygame.time.delay(1000)
                
    def draw_time(self):
        text = self.font1.render("Time: %02d:%02d"%(self.time/60, self.time%60), True, (255, 0, 0), (255, 255, 255))
        textrect = text.get_rect()
        textrect.centerx = 100
        textrect.centery = 30
        self.screen.blit(text, textrect)
    
    def draw_verticies(self):
        for vertex in self.Verticies:
            center = (vertex[1],vertex[2])
            pygame.draw.circle(self.screen,(0,0,200),center,12)
            #draw number of vertex
            text = self.font2.render("%d"%(vertex[0]), True, (255, 255, 255))
            textrect = text.get_rect()
            textrect.centerx = center[0]
            textrect.centery = center[1]
            self.screen.blit(text, textrect)
    
    def draw_edges(self):
        for edge in self.Edges:
            if len(edge[3]) > 2:
                #curve
                n = len(edge[3])
                count = 0
                while count < n-1:
                    start = (edge[3][count][0],edge[3][count][1])
                    end =  (edge[3][count+1][0],edge[3][count+1][1])
                    pygame.draw.line(self.screen,(200,0,0), start, end,2)
                    count += 1
            else:
                #straight line
                start = (edge[3][0][0],edge[3][0][1])
                end = (edge[3][1][0],edge[3][1][1])
                pygame.draw.line(self.screen,(200,0,0), start, end,2)
    
    def display_truck_locations(self,trucks):
        for truck in trucks:
            coordinates = truck.graph.get_coordinates(truck.location[1][0])
            step = float(truck.location[1][2])/float(truck.location[1][3])
            if len(truck.edge[3]) > 2:
                ## For curved edge
                length = 0
                n = len(truck.edge[3])
                count = 0
                while count < n-1:
                    length = length + math.sqrt((truck.edge[3][count+1][0]-truck.edge[3][count][0])**2 + (truck.edge[3][count+1][1] - truck.edge[3][count][1])**2)
                    count = count +1
                
                
                move = step*length
                count = 0
                while count < n-1:
                    current_segment = math.sqrt((truck.edge[3][count+1][0]-truck.edge[3][count][0])**2 + (truck.edge[3][count+1][1] - truck.edge[3][count][1])**2)
                    if move > current_segment:
                        move = move - current_segment
                        count = count + 1
                        continue
                    x2 = truck.edge[3][count+1][0]
                    y2 = truck.edge[3][count+1][1]
                    x1 = truck.edge[3][count][0]
                    y1 = truck.edge[3][count][1]
                    x1 = x1 + float(move/current_segment)*(x2-x1)
                    y1 = y1 + float(move/current_segment)*(y2-y1)
                    location = (int(x1),int(y1))
                    break
                if truck.location[1][2] == truck.location[1][3]:
                    location = truck.graph.get_coordinates(truck.location[1][1])
                    
                pygame.draw.circle(self.screen, (0,200,0),location,5)
                    
                
            else:
                ### ONLY WORKS IF PATH IS STRAIGHT ###
                x = coordinates[0] + step*truck.delta[0]
                y = coordinates[1] + step*truck.delta[1]
                location = (int(x),int(y))
                pygame.draw.circle(self.screen, (0,200,0),location,5)
        
        
            
            
            
            
            
            
            