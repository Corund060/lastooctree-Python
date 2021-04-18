import sys
import csv
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
    
class Plotter:
    
    def __init__(self, pointsToPlot):
        self.X=[]
        self.Y=[]
        self.Z=[]
        csvData = pointsToPlot
        self.X, self.Y, self.Z = csvData[:,0], csvData[:,1], csvData[:,2]

    def Plot3D(self):
        # Plot X,Y,Z
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        """ ax.plot_trisurf(self.X, self.Y, self.Z, color='white', edgecolors='grey', alpha=0.5) """
        ax.scatter(self.X, self.Y, self.Z, c='red')
        plt.show()