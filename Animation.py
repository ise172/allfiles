'''
Created on Mar 6, 2020

@author: Pierre, Andrew, Anna, Owen
'''

import pygame


class Animation():
    def __init__(self, edges, verticies):
        self.Edges = edges
        self.Verticies = verticies
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
            center = (int(vertex[1]*1500),int(vertex[2]*1500))
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
                    start = (int(edge[3][count][0]*1500),int(edge[3][count][1]*1500))
                    end =  (int(edge[3][count+1][0]*1500),int(edge[3][count+1][1]*1500))
                    pygame.draw.line(self.screen,(200,0,0), start, end,2)
                    count += 1
            else:
                #straight line
                start = (int(edge[3][0][0]*1500),int(edge[3][0][1]*1500))
                end = (int(edge[3][1][0]*1500),int(edge[3][1][1]*1500))
                pygame.draw.line(self.screen,(200,0,0), start, end,2)
    
    def display_truck_locations(self,trucks):
        for i in trucks:
            pygame.draw.circle(self.screen, (0,200,0),i.location,5)
        
        
            
            
            
            
            
            
            