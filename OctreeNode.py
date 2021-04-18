import numpy
import numpy as np
import OctreeData 

class OctreeNode:

    def __init__(self):
        self.NodeNo=0
        self.NodeDepth=0
        self.NodePoints=[]
        self.NodeParent=0 
        self.NodeCenter=[]
        self.ChildNodes=[] 
        self.NodeCorners=[]
    
    #Initiating composition of Octree by defining first node    
    def Compose(self, las_file):    
        print("Composing Octree for ", len(las_file.points)," points")
        self.NodeDepth = 0
        self.NodeParent = 0
        self.NodeNo = 1        

        minX = min(las_file.X)                
        maxX = max(las_file.X)

        minY = min(las_file.Y)                
        maxY = max(las_file.Y)                

        minZ = min(las_file.Z)                
        maxZ = max(las_file.Z)                       

        self.NodeCorners = [[minX, minY, maxZ],
                            [maxX, minY, maxZ],
                            [maxX, minY, minZ],
                            [minX, minY, minZ],
                            [minX, maxY, maxZ],
                            [maxX, maxY, maxZ],
                            [maxX, maxY, minZ],
                            [minX, maxY, minZ]]        

        self.NodePoints = np.vstack([las_file.X, las_file.Y, las_file.Z]).transpose()

        #//////////////////////////////////////////////////// Testing 
        #nodeCorners = new Point3D[8]{
        #    new Point3D { X=10, Y=10, Z=20 },
        #    new Point3D { X=20, Y=10, Z=20 },
        #    new Point3D { X=20, Y=10, Z=10 },
        #    new Point3D { X=10, Y=10, Z=10 },
        #    new Point3D { X=10, Y=20, Z=20 },
        #    new Point3D { X=20, Y=20, Z=20 },
        #    new Point3D { X=20, Y=20, Z=10 },
        #    new Point3D { X=10, Y=20, Z=10 }
        #}

        self.Divide(self)
        print("DONE")

        print("========================Octree info==================")
        print("Octree has a total of ", OctreeData.Data.NumberOfNodes," nodes")
        print("Octree has maximum depth of ", OctreeData.Data.MaxDepth, " levels")
        print("=====================================================")

        
    #Divide current node into 8 child nodes    
    def Divide(self, parentNode):

        #Divide untill parent node has less than 1000 points
        if (len(parentNode.NodePoints)<=1000):        
            return
        
        parentNode.NodeCenter = self.GetDivisionPoint(parentNode.NodeCorners)        
        for i in range(8):        
            currentNodeCorners = self.GetNodeCorners(parentNode, i+1)
            OctreeData.Data.NumberOfNodes=OctreeData.Data.NumberOfNodes+1
            if (OctreeData.Data.MaxDepth<parentNode.NodeDepth+1):
                OctreeData.Data.MaxDepth = parentNode.NodeDepth + 1
            newNode=OctreeNode()
            newNode.NodeNo = OctreeData.Data.NumberOfNodes,
            newNode.NodeDepth = parentNode.NodeDepth + 1
            newNode.NodeParent = parentNode.NodeNo
            newNode.NodeCorners = currentNodeCorners
            newNode.NodePoints = self.GetNodePoints(parentNode, currentNodeCorners)
            parentNode.ChildNodes.append(newNode)            
            self.Divide(newNode)
    
    
    #Assign parent points that are inside child node to child node    
    def GetNodePoints(self, parentNode, nodeCorners):
        rows = np.where((parentNode.NodePoints[:,0] >= nodeCorners[0][0]) & (parentNode.NodePoints[:,0] <= nodeCorners[1][0]) &
                        (parentNode.NodePoints[:,1] >= nodeCorners[3][1]) & (parentNode.NodePoints[:,1] <= nodeCorners[4][1]) &
                        (parentNode.NodePoints[:,2] >= nodeCorners[2][2]) & (parentNode.NodePoints[:,2] <= nodeCorners[1][2]))
        return parentNode.NodePoints[rows]        

    #Get division (center) point of the node 
    def GetDivisionPoint(self, nodeCorners):   
        x=  nodeCorners[0][0]+ (nodeCorners[1][0] - nodeCorners[0][0]) / 2
        y = nodeCorners[3][1]+ (nodeCorners[4][1] - nodeCorners[3][1]) / 2
        z = nodeCorners[2][2]+ (nodeCorners[1][2] - nodeCorners[2][2]) / 2
        return [x, y, z]
        
               

    #Get 8 corners of the child node according to its number    
    def GetNodeCorners(self, parent, childNo ):    
        parentCorners = parent.NodeCorners
        switcher = {
            1: #Tope near left     
            [[                                               parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[0][2] ], # Bottom near left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[0][2] ], # Bottom near right
                [                                           parent.NodeCenter[0],                                            parent.NodeCenter[1],                                            parent.NodeCenter[2] ], # Center
                [                                            parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Bottom far left
                [                                            parentCorners[4][0],                                             parentCorners[4][1],                                             parentCorners[4][2] ], # Top near left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1],                                             parentCorners[4][2] ], # Top near right
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Top far right
                [                                            parentCorners[0][0],                                             parentCorners[4][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ]],# Top far left        
            2: #Top near right             
            [[   parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[0][2] ],
                [                                            parentCorners[1][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[0][2] ],                        
                [                                            parentCorners[1][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[0][2]-parentCorners[3][2])/2 ],
                [                                           parent.NodeCenter[0],                                            parent.NodeCenter[1],                                             parent.NodeCenter[2]],
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1],                                              parentCorners[4][2]],
                [                                            parentCorners[1][0],                                             parentCorners[4][1],                                              parentCorners[4][2]],
                [                                            parentCorners[1][0],                                             parentCorners[4][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ],
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ]],            
            
            3: # Top far right            
                [[                                          parent.NodeCenter[0],                                            parent.NodeCenter[1],                                             parent.NodeCenter[2]], # Center
                [                                            parentCorners[1][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Bottom near right 
                [                                            parentCorners[1][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[7][2] ], # Bottom far right 
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[7][2]], # Bottom far left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Top near left
                [                                            parentCorners[1][0],                                             parentCorners[4][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Top near right                        
                [                                            parentCorners[1][0],                                             parentCorners[4][1],                                              parentCorners[7][2]], # Top far right                        
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1],                                             parentCorners[7][2]]], # Bottom far right                        
            
            4: # Top far left                
                [[                                           parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Botom near left
                [                                           parent.NodeCenter[0],                                            parent.NodeCenter[1],                                             parent.NodeCenter[2]], # Center
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[7][2]], # Bottom far right
                [                                            parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[7][2]], # Bottom far left
                [                                            parentCorners[0][0],                                             parentCorners[4][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Top near left                        
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Top near right
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[4][1],                                              parentCorners[7][2]], # Top far right
                [                                            parentCorners[0][0],                                             parentCorners[4][1],                                              parentCorners[7][2]]],# Top far left
            
            5: # Bottom near left            
                [[                                           parentCorners[0][0],                                             parentCorners[0][1],                                              parentCorners[0][2]], # Bottom near left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[0][1],                                              parentCorners[0][2]], # Bottom near right
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[0][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Bottom far right
                [                                            parentCorners[0][0],                                             parentCorners[0][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Bottom far left
                [                                            parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[0][2]], # Top near left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[0][2]], # Yop near right
                [                                           parent.NodeCenter[0],                                            parent.NodeCenter[1],                                             parent.NodeCenter[2]], # Center
                [                                            parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[0][2]-parentCorners[3][2])/2 ]],# Top far left
            
            
            6: # Bottom near right            
               [[parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[0][1],                                              parentCorners[0][2]], # Bottom near left
                [                                            parentCorners[2][0],                                             parentCorners[2][1],                                              parentCorners[0][2]], # Bottom near right
                [                                            parentCorners[2][0],                                             parentCorners[2][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Bottom far right
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[2][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Bottom far left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[0][2]], # Top left right
                [                                            parentCorners[2][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[0][2]], # Top near right
                [                                            parentCorners[2][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Top far right
                [                                           parent.NodeCenter[0],                                            parent.NodeCenter[1],                                            parent.NodeCenter[2]]], # Center
            
            7: # Bottom far right            
                [[parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[0][1],                                             parentCorners[0][2] ], # Bottom near left
                [                                             parentCorners[2][0],                                             parentCorners[2][1],  parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2], # Bottom near right
                [                                             parentCorners[2][0],                                             parentCorners[2][1],                                              parentCorners[2][2]], # Bottom far right
                [ parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[2][1],                                              parentCorners[2][2]], # Bottom far left
                [                                            parent.NodeCenter[0],                                            parent.NodeCenter[1],                                             parent.NodeCenter[2]], # Center
                [                                             parentCorners[1][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Top near right
                [                                             parentCorners[1][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[2][2]], # Top far right                                                                                                                                   
                [ parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                              parentCorners[2][2]]],# Top far left
            
            8: # Bottom far left            
                [[                                           parentCorners[0][0],                                             parentCorners[0][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Bottom near left
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[0][1], parentCorners[7][2]+(parentCorners[4][2]-parentCorners[7][2])/2 ], # Bottom near right
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2,                                             parentCorners[2][1],                                             parentCorners[2][2] ], # Bottom far right
                [                                            parentCorners[3][0],                                             parentCorners[3][1],                                             parentCorners[3][2] ], # Bottom far left
                [                                            parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2, parentCorners[7][2]+(parentCorners[0][2]-parentCorners[3][2])/2 ], # Top far left
                [                                           parent.NodeCenter[0],                                            parent.NodeCenter[1],                                             parent.NodeCenter[2]], # Center
                [parentCorners[0][0]+(parentCorners[1][0]-parentCorners[0][0])/2, parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[7][2] ], # Top far right
                [                                            parentCorners[0][0], parentCorners[0][1]+(parentCorners[4][1]-parentCorners[0][1])/2,                                             parentCorners[7][2] ]] # Top far left
            
        }
        return switcher.get(childNo, "Invalid child number")    