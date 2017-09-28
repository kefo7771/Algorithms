#Ken Ford
#CSCI 3104 Algorithms

#Homework 7

import matplotlib.pyplot as plt
import numpy as np
import timeit
import sys,math,copy

#create class for nodes of graphs
class graphNode(object):
    def __init__(self):
        self.nodeVal = 0        
        self.x = 0
        self.y = 0        
        self.connectedNodes = []
        self.color = ""
        self.pred = None
        self.start = 0
        self.finish = 0
        self.cycleStatus = False
        self.distance = 0
        self.visited = False

    def reloadGraph(self):
        self.color = ""
        self.pred = None
        self.start = 0
        self.finish = 0
        self.cycleStatus = False
        self.distance = 0
        self.visited = False

#create class that will save search sources and destinations
class searchVertices(object):
    def __init__(self):
        self.source = 0
        self.destination = 0

#function responsible for reading in and constructing graph from file
def constructGraph():

    fileName = sys.argv[-1]
    
    #check if file name is passed in, print error statement otherwise
    if not fileName:
        print "Missing file name as argument."
        return 0

    f = open(fileName,"r")

    #get line specifying vertex count and edge count    
    firstLine = f.readline()
    info = firstLine.split()
    #print info

    vertexCount = int(info[0])
    edgeCount = int(info[1].strip('\n'))  
    #print vertexCount
    #print edgeCount
    next(f)
    #create array to hold each graph node
    graphArr = []

    #create array to hold search indices
    searchArr = []

    for i, line in enumerate(f):
        if i % 1000 == 0:
            print i        
        if i < vertexCount:
            #print i
            #print line,
            currentSplit = line.split()
            currentNode = graphNode()
            
            currentNode.nodeVal = int(currentSplit[0])
            currentNode.x = int(currentSplit[1])
            currentNode.y = int(currentSplit[2])
            graphArr.append(currentNode)
            

            #print '******'
            #print currentNode.nodeVal
            #print currentNode.x
            #print currentNode.y

        if i > vertexCount and i <= vertexCount + edgeCount:
            #print line,
            edgeLine = line.split()
            source = int(edgeLine[0])
            destination = int(edgeLine[1].strip('\n'))
            #print source
            #print destination

            graphArr[source].connectedNodes.append(graphArr[destination])

            #for i in range(len(graphArr)):
                #if graphArr[i].nodeVal == source:
                    #graphArr[i].connectedNodes.append(graphArr[destination])


        if i > vertexCount + edgeCount + 1:
            #print line,
            searchLines = line.split()
            searchSource = int(searchLines[0])
            searchDestination = int(searchLines[1])

            searchOrder = searchVertices()
            searchOrder.source = searchSource
            searchOrder.destination = searchDestination

            searchArr.append(searchOrder)
  
       
    f.close()

    #print "************************"
    #for i in range(len(graphArr)):
        #print "Node Val: ",graphArr[i].nodeVal
        #print "X: ",graphArr[i].x
        #print "Y: ",graphArr[i].y
        #for j in range(len(graphArr[i].connectedNodes)):
			#print "Connected nodes ",i," ",graphArr[i].connectedNodes[j].nodeVal
        #print "*****************************"
    
    #for k in range(len(searchArr)):
        #print "Source: ",searchArr[k].source,", Destination: ",searchArr[k].destination

    #for i in range(len(weights)):
        #print "Source: ",weights[i].source,", Dest: ",weights[i].destination,", weight : ",weights[i].weight

    return graphArr,searchArr

#function provides depth first search of the graph
def DFS(G):
    #initialize color to white when not visited
    #predecessor to none as we haven't worked through the graph yet
    for i in range(len(G)):
        G[i].color = "White"
        G[i].pred = None

    time = 0
    topoList =[]

    for i in range(len(G)):
        if G[i].color == "White":
            #print G[i].nodeVal
            DFS_Visit(G,G[i],time,topoList)

    return topoList

#function calculates start,finish times for each node in DFS
def DFS_Visit(G, node,time,topoList):    
    time = time + 1
    node.start = time
    #print "Node ",node.nodeVal,", Start: ",node.start
    #mark visited, but not finished w/ gray
    node.color = "Gray"

    for i in range(len(node.connectedNodes)):
        currentNeighbor = node.connectedNodes[i]        
        #if neighbor has not been visited        
        if currentNeighbor.color == "White":
            node.connectedNodes[i].pred = node
            #print "Adjacent Node: ",node.connectedNodes[i].nodeVal,"'s predecessor: ",node.connectedNodes[i].pred.nodeVal
                        
            time = DFS_Visit(G,node.connectedNodes[i],time,topoList)
    
        #check for back edge        
        if currentNeighbor.color == "Gray":
            currentNeighbor.cycleStatus = True

    #mark as visited w/ black
    node.color = "Black"
    time = time + 1
    node.finish = time
    #print "Node: ",node.nodeVal," Start: ",node.start,", Finish: ",node.finish, "Color: ", node.color
    topoList.append(node)

    return time

#function provides a topological sort of a graph
#implements DFS in calculating finish times
def topoSort(graph):
    topologicalSort = DFS(graph)
    topologicalSort.reverse()

    #for i in range(len(topologicalSort)):
        #print topologicalSort[i].nodeVal

    return topologicalSort

#function provides boolean answer as to whether cyclce exists
#if an adjacent node was found to be gray in DFS, cycleStatus was marked True
def checkForCycle(graph):
    result = topoSort(graph)

    for i in range(len(result)):
        if result[i].cycleStatus == True:
            #print "Cycle exists"    
            return True

    #print "Cycle does not exist"    
    return False

#function determines which algorithm to choose based on cycle presence
#Dijkstra if cycle, DAG SSSP if no cycle
def handleCycleCase(graph,source,destination,status):
    value = {}
    if status == True:                  
            print "Dijkstra Selected"            
            value = DijkstraAlg(graph,graph[source],graph[destination])
    else:
            print "DAG SSSP Selected"           
            value = DAGSSSP(graph,graph[source],graph[destination])
            
    return value

#function is responsible for initializing each graph node's distance and predecessors before shortest path alg.
def initializeSingleSource(graph,source):
    for i in range(len(graph)):
        graph[i].distance = float("infinity")       
        graph[i].pred = None
        graph[i].visited = False    
    
    source.distance = 0

    return

#function checks distance relationship between a node and its predecessor
def relax(u,v):
    #if the adjacent node's distance is greater than the predecessor + edge weight, update it
    if v.distance > u.distance + distanceCalc(u,v):
        #print "U distance: ",u.distance,"U node: ",u.nodeVal       
        #print "First Distance: ",v.distance,"Current Node: ",v.nodeVal        
        v.distance = u.distance + distanceCalc(u,v)
        v.pred = u
        #print "Second Distance: ",v.distance,"Current Node: ",v.nodeVal," Pred: ",v.pred.nodeVal
    return

#function is responsible for maintaining heap property of priority queue
def minHeapify(A,i):
    l = 2*(i)
    r = 2*(i) + 1
    #check left child
    if l < len(A) and A[l].distance <= A[i].distance:
        smallest = l
    else: 
        smallest = i
    #check right child
    if r < len(A) and A[r].distance <= A[smallest].distance:
        smallest = r
    #if heap property is broken, fix it here
    if smallest != i:
        temp = A[i]
        A[i] = A[smallest]
        A[smallest] = temp
        minHeapify(A,smallest)

#function initally constructs the min heap for priority queue
def buildHeap(queue):
    heapSize = len(queue)
    halfWay = math.floor(heapSize/2)
    halfWay = int(halfWay)  
    for i in range(halfWay,-1,-1):
        minHeapify(queue,i)
    #for i in range(len(queue)):
        #print queue[i].nodeVal    
    return queue

#function takes the top value off the min heap and then re-heapifies it
def ExtractMin(queue):
    mini = queue[0]
    heapSize = len(queue)
    
    queue[0] = queue[heapSize - 1]
    queue.remove(queue[heapSize - 1])    
    heapSize -= 1
  
    #must maintain heap order here
    minHeapify(queue,0)
    return mini

#function gets Euclidean distance between two points
def distanceCalc(source,destination):
    distance = math.sqrt(((source.x - destination.x)**2) + ((source.y - destination.y)**2)) 
    return distance

#function that is responsible for getting shortest path when cycle exists
#resembles a BFS that picks and proceeds down the shortest available path 
def DijkstraAlg(graph,source,destination):
    tick = timeit.default_timer()        
    initializeSingleSource(graph,source)    
    print "Source: ",source.nodeVal," Dest: ",destination.nodeVal    
    path = []
    queue = buildHeap(graph)
    destinationReached = False

    while destinationReached == False:                   
        u = ExtractMin(queue)
        u.visted = True

        for i in range(len(u.connectedNodes)):
            relax(u,u.connectedNodes[i])
        if u.nodeVal == destination.nodeVal:
            destinationReached = True

    if destinationReached == True:
        path.append(destination)
        tmpNode = destination.pred
        while tmpNode != None:        
            path.append(tmpNode)
            tmpNode = tmpNode.pred

    path.reverse()
    #for i in range(len(path)):
        #print path[i].nodeVal

    finalDistance = destination.distance
    tock = timeit.default_timer()
    testTime = tock - tick
    print "End time for Dijkstra: ",testTime    
    
    return finalDistance,path

#function that gets shortest path when a cycle does not exist
def DAGSSSP(graph,source,destination):
    tick = timeit.default_timer()        
    totalDistance = 0
    path = []   
    #topologically sort the vertices of G
    topoList = topoSort(graph)
    #initialize single source
    initializeSingleSource(graph,source)
    for i in range(len(topoList)):
        currentNode = topoList[i]
        for j in range(len(topoList[i].connectedNodes)):
            relax(currentNode,topoList[i].connectedNodes[j])
    tmp = graphNode()
    tmp = graph[destination.nodeVal]
    while tmp.pred != None:        
        path.append(tmp)
        tmp = graph[tmp.pred.nodeVal]
    
    path.append(source)
    totalDistance = graph[destination.nodeVal].distance
    path.reverse()    
    #print totalDistance
    #for i in range(len(path)):
        #print path[i].nodeVal
    
    tock = timeit.default_timer()
    testTime = tock - tick
    print "End of DAG SSSP: ",testTime
    
    return totalDistance,path

#function that acts as graph constructor
def drawGraph(graph,path):        
    for i in range(len(graph)):
        #plot vertices and their labels
        plt.plot([graph[i].x],[graph[i].y],'ro')
        plt.text(graph[i].x + 25,graph[i].y + 25, str(graph[i].nodeVal))
        #plot edges between vertices        
        for j in range(len(graph[i].connectedNodes)):
            plt.plot([graph[i].x,graph[i].connectedNodes[j].x],[graph[i].y,graph[i].connectedNodes[j].y],'k')
    #plot shortest path and each edge's weight    
    for i in range(len(path) - 1):
        start = path[i]
        finish = path[i + 1]
        plt.plot([start.x,finish.x],[start.y,finish.y],'r',linewidth=6.0)
        dist = distanceCalc(start,finish)
        x_pos = ((start.x + finish.x) / 2)
        y_pos = ((start.y + finish.y) / 2)
        plt.text(x_pos,y_pos,str(dist),fontsize=18)
            

    plt.axis([0,2000,0,1000])    
    plt.show() 

    return


result = constructGraph()
graph = result[0]
graphSaved = copy.copy(graph)

search = result[1]
#print len(search)
sourceArr = []
destArr = []

for i in range(len(search)):
    tick = timeit.default_timer()    
    cycleResult = checkForCycle(graph)
    pathResult = handleCycleCase(graph,search[i].source,search[i].destination,cycleResult)
    tock = timeit.default_timer()
    testTime = tock - tick
    #print testTime
    graph = copy.copy(graphSaved)

    distance = pathResult[0]
    path = pathResult[1]
    drawGraph(graph,path)

    print distance
    for i in range(len(path)):
        print path[i].nodeVal





