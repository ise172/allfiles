from Classes.World import World

'''
For each order: 
- send truck to closest warehouse with the proper material type
- transport material (at least the number of tons needed(maybe more?) to the closest Production Line of the proper type
    - Along the shortest path
- wait for the processing time to be over
- transport finished product to the Final location



'''

myWorld = World()

print "\nEdges: ", myWorld.Edges 

print "\nVertices: ", myWorld.Verticies

print "\nGraph: ", myWorld.graph.neighbors, "\n\n"


myWorld.runSimulation(10)



