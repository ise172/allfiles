
#Import Classes that will be needed
from Classes.Trucks import Trucks
from Classes.Animation import Animation
from Classes.Graph import Graph
from  Classes.AbstractWorld import AbstractWorld
import pygame
pygame.font.init() 
import random



class World(AbstractWorld):
	#Initializes the World object
	def __init__(self):
		AbstractWorld.__init__(self)
		self.graph = Graph(self.Edges,self.Verticies)
		self.graph.create_graph()
		self.animation = Animation(self.graph)
		self.screen = pygame.display.set_mode((600, 800))
		self.clock = pygame.time.Clock()
		self.trucks = []

	#Main method that will run the simulation
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):
		
		#Get the lists of warehouses, production lines, and trucks that the company owns and prints each of them 
		Warehouses = self.getLocationOfWarehouses()
		print "Warehouses: ", Warehouses, "\n"
		ProductionLines = self.getProductionLines()
		print "Production Lines: ", ProductionLines, "\n"		
		trucks = self.getInitialTruckLocations()
		print "Vehicles: "
		for i,t in enumerate(trucks):
			print "vehicle %d: %s"%(i, str(t)) 
		
		self.animation.initialize_animation()  #Initializes the window that will display the animation of the simulation
		
		#This for loop keeps track of the time and one iteration is equivalent to a minute of the work day
		for t in xrange(initialTime,finalTime):
			print "\n\n\nTime: %02d:%02d"%(t/60, t%60) #prints the time
			self.animation.time = t  #updates the counter that tracks the time that is printed in the animation window
			newOrders = self.getNewOrdersForGivenTime(t) #Gets new orders
			if len(newOrders) != 0: #only enters this if statement if there are new orders
				print "\nNew orders:\n"
				#For each new order, print the production process, final location, path, and add a new truck
				for c in newOrders:
					print c
					print "Production Process: ", c.productionProcess
					print "Final Location: ", c.finalLocation
					## GENERATE TWO RANDOM VERTICES
					range = len(self.Verticies)
					start_node = self.Verticies[random.randrange(range)][0]
					end_node = self.Verticies[random.randrange(range)][0]
					while end_node == start_node: #Ensures that the start and end vertices are not the same
						end_node = self.Verticies[random.randrange(range)][0]
					## FIND THE SHORTEST PATH
					path = self.graph.dijkstra(start_node, end_node)
					## CREATE NEW TRUCK OBJECT AND ADD TO LIST OF TRUCKS
					self.trucks.append(Trucks(path, self.graph))
			#Update each truck's location and update the animation window 
			for i,truck in enumerate(self.trucks):
				truck.update_truck_location()
				print "location of truck ", i, ": ", truck.location
			self.animation.update_animation(self.trucks)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			pygame.display.update()	
			self.clock.tick(fps)