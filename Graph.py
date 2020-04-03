'''
Created on Mar 23, 2020

@author: Pierre
'''
import numpy as np
from openpyxl.descriptors.excel import Coordinate

class Graph:

    def __init__(self, edges, verticies):
        self.neighbors = {} # key - node, value - list of neighbours 
        self.cost = {}  # key - edge, value - cost
        self.Edges = edges
        self.Verticies = verticies

    def create_graph(self):
        for element in self.Edges:
            self.add_edge(element[0], element[1], element[2]) #change "1" to element[2] to get real distances/costs
    
    def add_edge(self,u,v,c): #this will add edge (u,v) with cost "c" to the graph
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

    def get_cost(self, u,v):
        if u > v:
          u, v = v, u
        if (u,v) in self.cost:
          return self.cost[(u,v)]
        return None

    def get_coordinates(self,node):
        for vertex in self.Verticies:
            if vertex[0] == node:
                coordinates = (int(vertex[1]*1500),int(vertex[2]*1500))
                return coordinates
        
    def dijkstra(self,start_node, end_node):
        d = {}
        for v in self.neighbors:
            d[v] = np.Inf
        d[start_node] = 0
        smallest_node = start_node
        permanent = {}
        pre = {}
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
        path.reverse()
        #print "From node ", start_node, " to node ", end_node    
        print "PATH: ", path
        #print "Length of path: ", d[end_node], " \n"
        return path
    
    def get_path(self,start_node,current_node,path,pre):
        if current_node == start_node:
            return path
        else:
            path.append(pre[current_node])
            self.get_path(start_node,pre[current_node],path,pre)
    
    
    '''  
    def get_coordinate_path(self,path):
        coordinate_path = []
        i = 0
        current_edge = 0
        while i < len(path)-1:
            for edge in self.Edges:
                if (edge[0] == path[i] and edge[1] == path[i+1]) or (edge[0] == path[i+1] and edge[1] == path[i]):
                    current_edge = edge
            if int(current_edge[3][0][0]*1500) != Graph.get_coordinates(self, edge[0])[0]:
                current_edge[3].reverse()
            for j,ix in enumerate(current_edge[3]):
                #if j > 0:
                #    coordinate_path.pop()
                coordinates = (int(ix[0]*1500),int(ix[1]*1500))
                coordinate_path.append(coordinates)
            
            i += 1
        return coordinate_path
    ''' 
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        