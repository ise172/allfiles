from Classes.World import World

'''
For each order: 
1.  Check if the least busy production line of the correct type has enough of the required material in its inventory (for each process in the order)
    - if it does not, send a truck to the closest warehouse of the correct type. It will fill up completely and bring the materials to the production line. (update the production line inventory)
2.  Start the production of the first process in the order (keep track of the time and update the inventory to account for materials used)
3.  Once the production is done, find the closest available truck to bring the WiP inventory to the next production line location.
4.  Repeat step 2-3 until there are no more additional processes to carry out.
5. Find the closest truck to bring the final product to the final location. Mark order as finished, and remove it from the list of openOrders.

Results for a full day: (as of 4/23)
sales:           $628,500,000
discount:        $204,700,000
transportation:  $2,534,805
holding:         $2,139,540
Profit:          $419,125,655

Results for a full day: (pick prodLines based on remaining production time rather than number of jobs -> decreased discounts by 20 million)
sales:            $628,500,000
discount:         $183,300,000
transportation:   $2,611,765
holding:          $2,139,540
Profit:           $440,448,695

'''

myWorld = World()


myWorld.runSimulation(10)



