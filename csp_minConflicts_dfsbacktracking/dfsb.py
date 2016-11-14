import sys
import random
import time
import copy

#check if all the nodes in the current assignment have a color
def checkCompleteAssignment( graph, assignment ):
    #check if assignment is complete
    for it in range(0,nNodes):
        if assignment[it] == -1:
            return False

    #check if assignment if correct
    for node1 in range(0,nNodes):
        for node2 in graph[node1]:
            if assignment[node1] == assignment[node2]:
                return False

    return True



#an iterative dfs implementation for csp
def dfsb( graph ):

    nodes = list(graph.keys())
    cAssign = [-1] * nNodes
    stack = []
    found = False

    #push in stack all possible colors of starting node
    for it1 in range(nColors - 1, -1, -1):
        cAssign = [-1]*len(nodes)
        cAssign[0] = it1
        stack.append((0,cAssign))

    count = 0;

    #iterative dfs using explicit stack
    while( len(stack) > 0 ):

        count += 1
        if time.time() - start_time >= 60:
            f = open(outputFile, 'w')
            f.write('No Answer')
            f.close()
            return

        #pop from the stack the uppermost node
        curr = stack.pop()
        currnode = curr[0]; currAssignment = curr[1]

        #check if assignment is complete
        if checkCompleteAssignment(graph,currAssignment) == True:
            print (currAssignment)
            f = open(outputFile, 'w')
            for ele in currAssignment:
                f.write(str(ele) + '\n')
            f.close()
            print ("number of iterations = " + str(count))
            print ("time taken = " + str(time.time() - start_time))
            found = True
            break

        adjcurr = list(graph[currnode])

        nextnode = -1

        #iterate over every adjacent node of the popped node and add them to stack
        for node in adjcurr:
            #only those nodes which have not been assigned a color (unvisited) are added to the stack
            if currAssignment[node] == -1:
                nextnode = node
            if nextnode >= 0:
                #reduce the domain of colors that the node can take depending upon its neighbors
                colors = list(range(0, nColors))
                adjn = list(graph[nextnode])
                for node2 in adjn:
                    if currAssignment[node2] != -1:
                        if (currAssignment[node2]) in colors:
                            colors.remove(currAssignment[node2])

                #add the node to the stack with every possible color it can take (inclusive of previous assignments)
                for colortoadd in reversed(colors):
                    newAssignment = list(currAssignment)
                    newAssignment[nextnode] = colortoadd
                    stack.append((nextnode, newAssignment))


    if found == False:
        f = open(outputFile, 'w')
        f.write('No Answer')
        f.close()

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

    #print(graph)
    return graph

count = 0
arc_prunes = 0;

def dfsb_improved(graph, curr_assignment, domain):

    if time.time() - start_time >= 60:
        f = open(outputFile, 'w')
        f.write('No Answer')
        f.close()
        return

    global count; global arc_prunes
    count = count + 1;
    if checkCompleteAssignment(graph,curr_assignment) == True:
        print (curr_assignment)
        print ('recursive calls= ' + str(count))
        print ('time taken = ' + str(time.time() - start_time))
        print('arc prunes = ' + str(arc_prunes))
        return True

    unassigned_vars = []
    for i in range(0,nNodes):
        if curr_assignment[i] == -1:
            unassigned_vars.append(i)

    #find the node with minimum remaining values
    mrvNode = -1; minR = 100000000
    mrvNodeList = []
    for node in unassigned_vars:
        temp = len((domain[node]))
        if temp < minR and temp > 0:
            minR = temp
    for node in unassigned_vars:
        if len(domain[node]) == minR:
            mrvNodeList.append(node)

    # mrvNode = random.choice(mrvNodeList)
    mrvNode = mrvNodeList[-1]

    #order the values accroding to least constraint on other unassigned variables
    numValues = len(domain[mrvNode])
    orderedValues = []
    for i in range(0,numValues):
        currVal = domain[mrvNode][i]
        numConstraintReductions = 0
        for node in list(graph[mrvNode]):
            if curr_assignment[node] == -1:
                if domain[node].__contains__(currVal):
                    numConstraintReductions += 1
        valueNumConstPair = [numConstraintReductions, currVal]
        orderedValues.append(valueNumConstPair)

    orderedValues.sort()
    values = [pair[1] for pair in orderedValues]

    #values is the colors sorted according to the number of constraints on the adjacent nodes
    for value in values:

        consistent = True
        for node in (graph[mrvNode]):
            if curr_assignment[node] == value :
                consistent = False

        if consistent == True:
            newAssignment = copy.deepcopy(curr_assignment)
            newAssignment[mrvNode] = value
            newDomain = copy.deepcopy(domain)
            newDomain[mrvNode] = []
            newDomain[mrvNode].append(value)

            # propagate constraints according to ac3
            acqueue = []
            for node in range(0,nNodes):
                adjNodes = list(graph[node])
                for nodej in adjNodes:
                    acqueue.insert(0,[node,nodej])

            cont = False;
            while len(acqueue) > 0 and cont == False:
                arc = acqueue.pop()

                removed = False;
                xi = arc[0]; xj = arc[1]
                for color in newDomain[xi]:
                    domainxj = list(newDomain[xj])
                    if len(domainxj) == 1:
                        if domainxj[0] == color:
                            removed = True
                            newDomain[xi].remove(color)
                            arc_prunes += 1
                            if len(newDomain[xi]) == 0:
                                cont = True
                            break

                if removed == True:
                    for adjnod in list(graph[xi]):
                        acqueue.insert(0,[adjnod, xi])

            if cont == True:
                continue

            result = dfsb_improved(graph, newAssignment, newDomain)

            if result == True:
                return result

    return False

f = open('debug.txt', 'w')

inputFile = sys.argv[1]
outputFile = sys.argv[2]
algo = sys.argv[3]

start_time = time.time();

if algo == "0":
    graph = createGraph(inputFile)
    dfsb(graph)

if algo == "1":
    graph = createGraph(inputFile)
    assignment = [-1] * nNodes
    domain = [];

    for i in range(0, nNodes):
        domain.append(list(range(0,nColors)))

    res = dfsb_improved(graph, assignment, domain)
    if res == False:
        f = open(outputFile, 'w')
        f.write('No Answer')
        f.close()











