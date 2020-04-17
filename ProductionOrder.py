'''
Created on Apr 17, 2020

@author: Pierr
'''

class ProductionOrder:
    
    def __init__(self,id,prodProcess,finalLocation,lineLocations):
        self.ID = id
        self.prodProcess = prodProcess
        self.finalLocation = finalLocation
        self.finished = False
        self.currentProcess = self.prodProcess[0]
        self.lineLocations = lineLocations
        self.currentProcessProgress = [0,self.currentProcess['processingTime']]
    
    
    
    def __str__(self):
        return "\nOrder "+str(self.ID)+": " + str(self.prodProcess)+ "\n    Current process: "+ str(self.currentProcess)+" is " +str(self.currentProcessProgress[0])+" out of "+str(self.currentProcessProgress[1])+" minutes complete at the production line located at node "+str(self.lineLocations[0])