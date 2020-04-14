from Classes.World import World



myWorld = World()

print "\nEdges: ", myWorld.Edges 

print "\nVertices: ", myWorld.Verticies

print "\nGraph: ", myWorld.graph.neighbors, "\n\n"


myWorld.runSimulation(10)



