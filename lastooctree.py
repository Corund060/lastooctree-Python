import sys
import os
from plotter import Plotter
from os import path

def main(argv):
        
    currentDir = os.path.dirname(os.path.abspath(__file__))
    filePath = os.path.join(currentDir, argv[0])

    if (len(argv)!=0 and path.exists(filePath)) :        
                 
        import numpy as np
        from laspy.file import File
        inFile = File(filePath, mode='r')         
        print("========================Header info==================")
        print("File signature: ", inFile.header.file_signature)
        print("Las file format version: ", inFile.header.major_version,".",inFile.header.minor_version)
        print("File creation: ", inFile.header.date)
        print("X,Y,Z scale factors : ", inFile.header.scale[0],"; ", inFile.header.scale[1],"; ", inFile.header.scale[2])
        print("X,Y,Z offsets : ", inFile.header.offset[0],"; ", inFile.header.offset[1],"; ", inFile.header.offset[2])
        print("Max X, Min X ------- ", max(inFile.x),": ", min(inFile.x))
        print("Max Y, Min Y ------- ", max(inFile.y),": ", min(inFile.y))
        print("Max Z, Min Z ------- ", max(inFile.z),": ", min(inFile.z))
        print("=====================================================")

        #Compose Octree object from data object        
        from OctreeNode import OctreeNode
        octree = OctreeNode()
        octree.Compose(inFile)

        """ PlotIt(octree) """
        
    else :
        print("Error: LAS file not provided/not found")

def PlotIt(octree):
    import numpy as np        
    points=[]
    for node in octree.ChildNodes:      
        if (len(points)==0):
            points = np.array(node.NodeCorners)
        else:         
            """ arr=np.array(node.NodeCorners)
            points=np.concatenate((points, arr))  """
        for nextNode in node.ChildNodes:
            """ arr=np.array(nextNode.NodeCorners)
            points=np.concatenate((points, arr)) """
            if (len(nextNode.NodePoints)<1000):
                arr=np.array(nextNode.NodeCorners)
                points=np.concatenate((points, arr))
                points=np.concatenate((points, nextNode.NodePoints))                
    plot = Plotter(points)
    plot.Plot3D()

if __name__ == "__main__":
    main(sys.argv[1:])