from Classes.World import World


# GitHub: to work on the code together online

myWorld = World()

print "\nEdges: ", myWorld.Edges 

print "\nVertices: ", myWorld.Verticies

print "\nGraph: ", myWorld.graph.neighbors, "\n\n"


myWorld.runSimulation(10)



