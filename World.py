from  Classes.AbstractWorld import AbstractWorld
from Animation import Animation
from Graph import Graph
import pygame
from Classes.Trucks import Trucks
pygame.font.init() 
import random
import numpy as np
import time


class World(AbstractWorld):
	
	def __init__(self):
		AbstractWorld.__init__(self)
		self.animation = Animation(self.Edges,self.Verticies)
		self.graph = Graph(self.Edges,self.Verticies)
		self.screen = pygame.display.set_mode((600, 800))
		self.clock = pygame.time.Clock()
		self.trucks = []


	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):
		self.graph.create_graph()
		#print "\nGraph: ", self.graph.neighbors , "\n"
		
		trucks = self.getInitialTruckLocations()
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t)) 



		self.animation.initialize_animation()
		
		for t in xrange(initialTime,finalTime):
			self.animation.time = t
			for truck in self.trucks:
				truck.update_truck_location()
				print "location: ", truck.location
			self.animation.update_animation(self.trucks)
			
			
			newOrders = self.getNewOrdersForGivenTime(t)
			print "\n\n\nTime: %02d:%02d"%(t/60, t%60)
			# each minute we can get a few new orders
			if len(newOrders) != 0:
				print "\nNew orders:\n"
				for c in newOrders:
					print c
					
					## GENERATE TWO RANDOM VERTICES
					range = len(self.Verticies)
					#start_node = self.Verticies[random.randrange(range)][0]
					start_node = 122 #TEST CASE
					end_node = 1
					#end_node = self.Verticies[random.randrange(range)][0]
					while end_node == start_node: #Ensures that the start and end vertices are not the same
						end_node = self.Verticies[random.randrange(range)][0]
					
					## FIND THE SHORTEST PATH
					path = self.graph.dijkstra(start_node, end_node)
					
					if len(self.trucks) == 0:
						self.trucks.append(Trucks(path, self.graph))
			
	
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
           	pygame.display.update()	
           	self.clock.tick(fps)
        
