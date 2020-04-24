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
        if d == 'OneWayA': 
            #only from first to second
            self.cost[(u,v)] = c

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
        
        for edge in self.Edges: 
            if edge[4] == 'B':
                D[map[edge[0]],map[edge[1]]] = self.get_cost(edge[0],edge[1])
                D[map[edge[1]],map[edge[0]]] = self.get_cost(edge[1],edge[0])
            if edge[4] == 'OneWayB':
                D[map[edge[1]],map[edge[0]]] = self.get_cost(edge[1],edge[0])
            if edge[4] == 'OneWayA':
                D[map[edge[0]],map[edge[1]]] = self.get_cost(edge[0],edge[1]) 

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
        return path 
    
    # Finds the shortest path from a start node to an end node and returns the cost of the path 
    def floyd_warshall_length(self, path):
        cost = 0
        for i in range(0,len(path)-2):
            cost = cost + self.get_cost(path[i],path[i+1])
        return cost       
    
    
    
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
