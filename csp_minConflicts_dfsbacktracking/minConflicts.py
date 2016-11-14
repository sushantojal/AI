import sys
import random
import math
import time

#helper function which calculates the number of conflicts in the current graph given an assignment
def getNumConflicts( graph, assignment ):

    numConflicts = 0
    for currNode in range(0, nNodes):
        adjNodes = graph[currNode]
        for adjNode in adjNodes:
            if assignment[adjNode] == assignment[currNode]:
                numConflicts += 1

    numConflicts = numConflicts
    return numConflicts


#implementation of the minconflicts algorithm
def minConflicts (graph):

    #initial assignment to all nodes is random
    currAssignment = list(range(0,nNodes))
    for i in range (0, nNodes):
        color = random.randint(0,nColors - 1)
        currAssignment[i] = color

    numTries = 1000000000
    tryThreshold = 6000

    # find number of conflicts in the current assignments
    numConflict = getNumConflicts(graph, currAssignment)
    if numConflict == 0 :
        print (currAssignment)
        print('0')
        f = open(outputFile, 'w')
        for ele in currAssignment:
            f.write(str(ele) + '\n')
        f.close()
        return


    constraintViolatingNodes = []

    for iter in range (0, numTries):

        #terminate if no solution even after 60 seconds
        if (time.time() - start_time) >= 60:
            f = open(outputFile,'w')
            f.write('No answer')
            f.close()
            return

        #create a set of nodes which violate constraints
        for node in range (0, nNodes):
            adjNodes = graph[node]
            for adjNode in adjNodes:
                if currAssignment[adjNode] == currAssignment[node]:
                    if node not in constraintViolatingNodes:
                        constraintViolatingNodes.append(node)
                        break

        #choose a node randomly from this set
        luckyNode = constraintViolatingNodes[random.randint(0,len(constraintViolatingNodes)-1)]


        # if number of tries exceed tryThreshold begin from random assignment of colors to variables
        if (iter % tryThreshold ) == 0 and iter != 0:
            print ('randomising..')
            for i in range(1,random.randint(0,math.floor(nNodes/5))):
                currAssignment[random.randint(0,nNodes - 1)] = random.randint(0,nColors-1)

            numConflict = getNumConflicts(graph, currAssignment)
            if numConflict == 0:
                print(currAssignment)
                print("number of iterations = " + str(iter))
                print("time taken = " + str(time.time() - start_time))
                f = open(outputFile, 'w')
                for ele in currAssignment:
                    f.write(str(ele) + '\n')
                f.close()
                return

            continue

        #greedy selection of colors form among colors which reduce the number of conflicts
        possibleGreedyColors = [];
        for color in range(0, nColors):
            newAssignment = list(currAssignment)
            newAssignment[luckyNode] = color
            newNumConflicts = getNumConflicts(graph, newAssignment)
            if newNumConflicts <= numConflict:
                numConflict = newNumConflicts
                if numConflict == 0:
                    print(newAssignment)
                    print("number of iterations = " + str(iter))
                    print("time taken = " + str(time.time() - start_time))
                    f = open(outputFile, 'w')
                    for ele in newAssignment:
                        f.write(str(ele) + '\n')
                    f.close()
                    return

        for color in range(0, nColors):
            newAssignment = list(currAssignment)
            newAssignment[luckyNode] = color
            newNumConflicts = getNumConflicts(graph, newAssignment)
            if newNumConflicts == numConflict:
                possibleGreedyColors.append(color)

        if( len(possibleGreedyColors) != 0 ):
            color = random.choice(possibleGreedyColors)
            currAssignment[luckyNode] = color

    return



nColors = 0
nNodes = 0
nEdges = 0

#create a adjacency list representation of graph using dictionary
def createGraph(inputFile):

    global nColors, nNodes, nEdges

    f = open(inputFile, 'r')
    it = 0; n = 0; m = 0; k = 0
    inf = []; graph = {}; nodes = []
    for line in f:
        if it == 0:
            inf = line.strip().split()
            n = int(inf[0]); m = int(inf[1]); nColors = int(inf[2]); nNodes = n; nEdges = m
            it = 1
            for x in range (0, n):
                graph[x] = []
        else:
            inf = line.strip().split()
            node1 = int(inf[0]); node2 = int(inf[1])
            #undirected graph
            graph[node1].append(node2)
            graph[node2].append(node1)

    return graph


start_time = time.time();
inputFile = sys.argv[1]
outputFile = sys.argv[2]

graph = createGraph(inputFile)
minConflicts(graph)