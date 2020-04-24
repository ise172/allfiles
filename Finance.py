'''
Created on Apr 23, 2020

@author: Pierre
'''

class Finance: 
    #initializes the revenue, cost, and profit as zero
    def __init__(self):
        self.profit = 0
        self.sales = 0
        self.discount = 0
        self.transportationCosts = 0
        self.holdingCosts = 0

    #Updates the revenue given the total order time (price minus the late fee)
    def update_revenue(self,time):
        if time <= 60:
            lateFee = 0
        else:
            lateFee = 100000*((time - 60)/30 + 1)
        self.sales = self.sales + 1500000
        self.discount = self.discount + lateFee
        self.profit = self.sales-self.discount-self.transportationCosts-self.holdingCosts
    
    # Updates the cost by summing the costs of all of the production lines and trucks
    def update_costs(self,trucks,productionLines):
        tcost = 0
        hcost = 0
        for truck in trucks:
            tcost = tcost + truck.transportationCost
        for line in productionLines:
            hcost = hcost + line.holdingCost
        self.transportationCosts = tcost
        self.holdingCosts = hcost
        self.profit = self.sales-self.discount-self.transportationCosts-self.holdingCosts
        
    #Prints the finances
    def __str__(self):
        return "sales: "+str(self.sales)+"\ndiscount: "+str(self.discount)+"\ntransportation: "+str(self.transportationCosts)+"\nholding: "+str(self.holdingCosts)+"\nProfit: "+str(self.profit)