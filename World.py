
#Import Classes that will be needed
from Classes.Truck import Truck
from Classes.Animation import Animation
from Classes.Graph import Graph
from Classes.AbstractWorld import AbstractWorld
from Classes.Warehouse import Warehouse
from Classes.ProductionLine import ProductionLine
from Classes.ProductionOrder import ProductionOrder
import pygame
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
		self.prodLines = []
		self.warehouses = []
		self.openOrders = []

	#Main method that will run the simulation
	def runSimulation(self, fps=1, initialTime=5*60, finalTime=23*60):
		
		#Get the lists of warehouses, production lines, and trucks that the company owns 
		Warehouses = self.getLocationOfWarehouses()
		ProductionLines = self.getProductionLines()
		Trucks = self.getInitialTruckLocations()
		# Create objects for each production line, warehouse, and truck
		for w in Warehouses:
			self.warehouses.append(Warehouse(w['location'],w['type']))
		for p in ProductionLines:
			self.prodLines.append(ProductionLine(p['location'],p['type'],['capacityOfMaterial[tons]']))	
		for i,t in enumerate(Trucks):
			self.trucks.append(Truck(t.currentPossition[1],self.graph,t.capacity,i))
		# Print the production lines, warehouses, and trucks
		print "\nProduction Lines: ", ProductionLines, "\n" , "Warehouses: ", Warehouses, "\n"
		print "Vehicles: "
		for i,t in enumerate(Trucks):
			print "vehicle %d: %s"%(i, str(t))
		#Initialize the graph and print the edges, verticies, and the graph (as a list of neighbors)
		self.graph.create_graph(Warehouses,ProductionLines)
		print "\nEdges: ", self.graph.Edges 
		print "\nVertices: ", self.graph.Verticies
		print "\nGraph: ", self.graph.neighbors, "\n\n"
		# Initialize the floyd warshall algorithm to get all the shortest paths. And initialize the animation screen for the simulation
		self.graph.initialize_floyd_warshall()
		self.animation.initialize_animation(self.graph)
		
		
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
					
					#makes sure that the production line needed for each process has the necessary inventory, otherwise, stocks up 
					jobLocations = []
					for process in c.productionProcess:
						jobs,index = 100,0
						for i,p in enumerate(self.prodLines):
							if p.type == process['processinLine']:
								if p.currentJobs < jobs:
									jobs = p.currentJobs
									index = i
									location = p.location
						
						if self.prodLines[index].inventory[process['resourceNeeded']] < process['materialNeeded[tons]'] and not self.prodLines[index].shipmentOnWay:
							self.prodLines[index].get_resources(process['resourceNeeded'],process['materialNeeded[tons]'],self.trucks,self.graph,self.warehouses)
						jobLocations.append(location)
								
					#Create an order object for this new order
					self.openOrders.append(ProductionOrder(c.id,c.productionProcess,c.finalLocation,jobLocations))
			
			#print list of open orders and their progress
			for order in self.openOrders:
				print order.__str__()
					
			#Update each truck's location and update the animation window 			
			for truck in self.trucks:
				truck.update_truck_location()
			self.animation.update_animation(self.trucks)
			
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					quit()
			pygame.display.update()	
			self.clock.tick(fps)
			
