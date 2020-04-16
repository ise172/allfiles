
#Import Classes that will be needed
from Classes.Trucks import Trucks
from Classes.Animation import Animation
from Classes.Graph import Graph
from  Classes.AbstractWorld import AbstractWorld
import pygame
from networkx.algorithms.shortest_paths.dense import floyd_warshall
pygame.font.init() 
import random



class World(AbstractWorld):
	#Initializes the World object
	def __init__(self):
		AbstractWorld.__init__(self)
		self.graph = Graph(self.Edges,self.Verticies)
		self.animation = Animation(self.graph)
		self.screen = pygame.display.set_mode((600, 800))
		self.clock = pygame.time.Clock()
		self.trucks = []

	#Main method that will run the simulation
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):
		
		#Get the lists of warehouses, production lines, and trucks that the company owns and prints each of them 
		Warehouses = self.getLocationOfWarehouses()
		ProductionLines = self.getProductionLines()
		print "Production Lines: ", ProductionLines, "\n" , "Warehouses: ", Warehouses, "\n"		
		trucks = self.getInitialTruckLocations()
		print "Vehicles: "
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t))
			self.trucks.append(Trucks(t.currentPossition[1],self.graph,t.capacity))#creates truck objects for each truck
		
		self.graph.create_graph(Warehouses,ProductionLines)
		self.graph.initialize_floyd_warshall()
		
		self.animation.initialize_animation(self.graph)  #Initializes the window that will display the animation of the simulation
		
		#This for loop keeps track of the time and one iteration is equivalent to a minute of the work day
		for t in xrange(initialTime,finalTime):
			print "\n\n\nTime: %02d:%02d"%(t/60, t%60) #prints the time
			self.animation.time = t  #updates the counter that tracks the time that is printed in the animation window
			newOrders = self.getNewOrdersForGivenTime(t) #Gets new orders
			if len(newOrders) != 0: #only enters this if statement if there are new orders
				print "\nNew orders:\n"
				#For each new order, print the production process, final location, path, and add a new truck
				for c in newOrders:
					print "\n", c
					print "Production Process: ", c.productionProcess
					print "Final Location: ", c.finalLocation
					
					'''
					#Tests to see if the floyd marshall algorithm is working (issue: it works for some paths but seems to have trouble with some paths/ one way roads and returns a path length of infinity, even though dijkstra can find a shortest path)
					start = random.randrange(1,100)
					end = random.randrange(1,100)
					print "From ", start, " to ", end
					path1 = self.graph.floyd_warshall(start, end)
					print "floyd warshall path: ", path1
					path2 = self.graph.dijkstra(start, end)
					print "dijkstra path: ", path2
					'''
					
					##Find truck that is closest to warehouse of correct type
					self.graph.find_truck_to_get_material_from_warehouse_to_productionLine(c.productionProcess, self.trucks)
					

					
			#Update each truck's location and update the animation window 			
			for i,truck in enumerate(self.trucks):
				truck.update_truck_location()
			self.animation.update_animation(self.trucks)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			pygame.display.update()	
			self.clock.tick(fps)