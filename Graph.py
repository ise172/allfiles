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

    #Creates the graph by scaling the coordinate values and adding the edges to the graph
    def create_graph(self):
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
            self.add_edge(element[0], element[1], element[2])
    
    #Adds the edge (u,v) with cost "c" to the graph if v and u are not in the graph already
    def add_edge(self,u,v,c): 
        if u not in self.neighbors:
            self.neighbors[u]=[]
        if v not in self.neighbors:
            self.neighbors[v]=[]
        if u > v:
            u, v = v, u
        if (u,v) not in self.cost:
            self.neighbors[u].append(v)
            self.neighbors[v].append(u)
            self.cost[(u,v)] = c

    #Returns the cost of edge (u,v)
    def get_cost(self, u,v):
        if u > v:
            u, v = v, u
        if (u,v) in self.cost:
            return self.cost[(u,v)]
        return None

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
        print "PATH: ", path, "\nLength of path: ", d[end_node], " \n"
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
