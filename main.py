from Classes.World import World

'''
For each order: 
1.  Check if the least busy production line of the correct type has enough of the required material in its inventory (for each process in the order)
    - if it does not, send a truck to the closest warehouse of the correct type. It will fill up completely and bring the materials to the production line. (update the production line inventory)
2.  Start the production of the first process in the order (keep track of the time and update the inventory to account for materials used)
3.  Once the production is done, find the closest available truck to bring the WiP inventory to the next production line location.
4.  Repeat step 2-3 until there are no more aditional processes to carry out.
5. Find the closest truck to bring the final product to the final location. Mark order as finished, and remove it from the list of openOrders.

'''

myWorld = World()

#print "\nEdges: ", myWorld.Edges 
#print "\nVertices: ", myWorld.Verticies
#print "\nGraph: ", myWorld.graph.neighbors, "\n\n"


myWorld.runSimulation(10)



