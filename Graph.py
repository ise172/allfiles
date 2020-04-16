'''
Created on Mar 23, 2020

@author: Pierre
'''
import numpy as np

class Graph:
    #Initializes the graphs
    def __init__(self, edges, verticies):
        self.neighbors = {} # key - node, value - list of neighbors 
        self.cost = {}  # key - edge, value - cost
        self.Edges = edges
        self.Verticies = verticies
        self.Warehouses = []
        self.ProductionLines = []
        self.FW_next = {}


    #Creates the graph by scaling the coordinate values and adding the edges to the graph
    def create_graph(self,warehouses,productionLines):
        self.Warehouses = warehouses
        self.ProductionLines = productionLines        
        #These first two while loops scale the values to fit the size of the window by multiplying every coordinate value by 1500
        i,j = 0,0
        while i < len(self.Verticies):
            self.Verticies[i][1] = int(self.Verticies[i][1]*1500)
            self.Verticies[i][2] = int(self.Verticies[i][2]*1500)
            i = i + 1
        while j < len(self.Edges):
            k = 0
            while k < len(self.Edges[j][3]):
                self.Edges[j][3][k] = (int(self.Edges[j][3][k][0]*1500), int(self.Edges[j][3][k][1]*1500))
                k = k + 1
            j = j + 1
        #Adds each edge to the graph object
        for element in self.Edges:
            self.add_edge(element[0], element[1], element[2], element[4])
    
    
    #Adds the edge (u,v) with cost "c" to the graph if v and u are not in the graph already. d is  the direction of the edge
    def add_edge(self,u,v,c,d): 
        if u not in self.neighbors:
            self.neighbors[u]=[]
        if v not in self.neighbors:
            self.neighbors[v]=[]
        if ((u,v) not in self.cost) and ((v,u) not in self.cost):
            self.neighbors[u].append(v)
            self.neighbors[v].append(u)
        if d == 'B':
            #both directions
            self.cost[(u,v)] = c
            self.cost[(v,u)] = c
        if d == 'OneWayB':
            #only from second node to first
            self.cost[(v,u)] = c
            #self.cost[(u,v)] = np.inf
        if d == 'OneWayA': 
            #only from first to second
            self.cost[(u,v)] = c
            #self.cost[(v,u)] = np.inf

    #Returns the cost of edge (u,v)
    def get_cost(self, u,v):
        if (u,v) in self.cost:
            return self.cost[(u,v)]
        return np.inf

    #Returns the coordinates of a given node
    def get_coordinates(self,node):
        for vertex in self.Verticies:
            if vertex[0] == node:
                coordinates = (vertex[1],vertex[2])
                return coordinates
        
    #Returns true if the current coordinates are the coordinates of a vertex, otherwise returns false
    def is_vertex(self,coordinates):
        for vertex in self.Verticies:
            if (coordinates == (vertex[1],vertex[2])):
                return True
            else:
                return False
    
    # Runs the Floyd Warshall algorithm to find the shortest path from every combination of nodes
    def initialize_floyd_warshall(self):
        n = len(self.neighbors)
        D = np.ones([n,n])*np.inf
        D[range(n),range(n)] = 0
        
        map={}
        V = sorted(self.neighbors.keys())
        for i,v in enumerate(V):
            map[v]=i
        
        for e in self.cost:
            D[map[e[0]],map[e[1]]] = self.cost[e]
            D[map[e[1]],map[e[0]]] = self.cost[e]
        
        
        for i in V:
            for j in V:
                self.FW_next[i,j] = '?'
        
        for e in self.cost:
            self.FW_next[e[0],e[1]] = e[1]
            self.FW_next[e[1],e[0]] = e[0]
        
        for k in V:
            for i in V:
                for j in V:
                    if D[map[i],map[k]]+D[map[k],map[j]] < D[map[i],map[j]]:
                        D[map[i],map[j]] = D[map[i],map[k]]+D[map[k],map[j]]
                        self.FW_next[i,j] = self.FW_next[i,k]
    
    #Finds the shortest path from a start node to an end node using the next dictionary of the floyd marshall algorithm
    def floyd_warshall(self,fromNode,toNode):
        cost = 0
        path = [] 
        while fromNode != toNode:
            path.append(fromNode)
            temp = fromNode
            fromNode = self.FW_next[fromNode,toNode]
            cost = cost + self.get_cost(temp, fromNode)
        path.append(toNode)
        print "Cost of floyd warshall path: ", cost
        return path
        
            
    
    #This function is dijkstra's shortest path algorithm that returns the path from a start node to an end node
    def dijkstra(self,start_node, end_node):
        d = {}
        for v in self.neighbors:
            d[v] = np.Inf
        d[start_node] = 0
        smallest_node = start_node
        permanent,pre = {},{}
        while smallest_node != end_node:
            smallest_value = np.Inf
            smallest_node = None
            for v in d:
                if v not in permanent and (d[v] < smallest_value):
                    smallest_value = d[v]
                    smallest_node = v
            permanent[smallest_node] = True
            for nv in self.neighbors[smallest_node]:
                if nv not in permanent:
                    proposed_distance = d[smallest_node] + self.get_cost(smallest_node,nv)
                    if proposed_distance < d[nv]:
                        d[nv] = proposed_distance
                        pre[nv] = smallest_node
        path = []
        path.append(end_node)
        self.get_path(start_node,end_node,path,pre)    
        path.reverse()     #get_path() returns the path in reverse order so this line fixes that
        #print "PATH: ", path, "\nLength of path: ", d[end_node], " \n"
        print "Cost of dijkstra path: ", d[end_node]
        return path
    
    #This is a recursive function that is called within the dijkstra algorithm that gets the path from the list of previous nodes
    def get_path(self,start_node,current_node,path,pre):
        if current_node == start_node:
            return path
        else:
            path.append(pre[current_node])
            self.get_path(start_node,pre[current_node],path,pre)
    
    
    #This function loops through every edge and return the edge from a start node to an end node
    def get_edge(self, start, end):
        for edge in self.Edges:
            if (edge[0]==start and edge[1]==end) or (edge[0]==end and edge[1]==start): 
                if ((edge[3][0][0],edge[3][0][1]) == self.get_coordinates(start)):
                    return edge
                else: #reverses the list of coordinates if the start node and end node are in the wrong order
                    edge[3].reverse()
                    return edge

    #This function finds the truck that is closest to the a warehouse with the correct resource. Then, is finds the shortest path from that truck's current location to that ware house, and adds the shortest path
    # from that warehouse to the closest proper production line. Assigns this full path to the truck. (ie: The truck will pick up supplies from the warehouse and bring them to the production line)
    def find_truck_to_get_material_from_warehouse_to_productionLine(self,prodProcess,trucks):
        #does this for each part of the production process so that the material is already waiting at the production line when needed.
        for process in prodProcess:
            print "\nprocess: ", process
            distance,index,count = 1000,0,0
            warehouses,productionLines = [], []
            for warehouse in self.Warehouses: #Finds list the warehouses that can be used for this process
                if warehouse['type'] == process['resourceNeeded']:
                    warehouses.append(warehouse)
            for prodLine in self.ProductionLines: # Finds list of the production lines that can be used for this process
                if prodLine['type'] == process['processinLine']:
                    productionLines.append(prodLine)
            for truck in trucks: # Loops through all of the trucks, if it does not have the capacity for the materials or if it is busy, the truck is skipped and the next one is considered
                if truck.capacity < process['materialNeeded[tons]'] or truck.occupied:
                    count = count + 1
                    continue
                for warehouse in warehouses: #for each warehouse that could be used, find the shortest path distance and update it if it is shorter than the current shortest distance
                    temp = self.dijkstra(truck.location[1][0],warehouse['location']) ##takes a long time/causes simulation to be slow!!
                    length = len(temp)
                    if length < distance:
                        distance = length
                        Wpath = temp
                        index = count #keeps track of which truck's path we need to update
                count = count + 1
            if not trucks[index].occupied: # if this truck is available, update the path, occupied boolean, and capacity
                trucks[index].path = Wpath
                trucks[index].occupied = True
                trucks[index].capacity = trucks[index].capacity - process['materialNeeded[tons]']
            else: # otherwise, return bc no trucks are available
                print "No available trucks"
                return
            distance = 1000
            for line in productionLines: #Similar process for the production line, except we know the truck and starting location, so we just need to find the path to the closes prod. line
                temp = self.dijkstra(Wpath[len(Wpath)-1],line['location'])
                length = len(temp)
                if length < distance:
                    distance = length
                    PLpath = temp
            PLpath.pop(0)
            while len(PLpath) > 0:
                trucks[index].path.append(PLpath.pop(0))
            print "path of truck ", index, ": ", trucks[index].path    # This the full path from the trucks original location to the production line, passing through the warehouse

