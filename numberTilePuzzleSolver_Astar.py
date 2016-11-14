import sys
import queue as Q
from copy import deepcopy
import time



#every list has the fvalues at index 0,
                    #state array at index 1
                    #location of blank tile at index 2
                    #actual cost value at index 3
                    #the string describing the path from root at index 4
find = 0
stateind = 1
blankind = 2
gind = 3
pathind = 4
usenaive = 0


#helper function to check if given node is the goal node
def goalnodecheck( currnode, dim ):
    goalstate = []
    if dim == 3:
        goalstate = [[1, 2, 3], [4, 5, 6], [7, 8, -1]]
    elif dim == 4:
        goalstate = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, -1]]

    if currnode[stateind] == goalstate:
        return True
    else:
        return False


#create and return a new node based on the curr state of the node and the action taken
def makenode( node, action, dim):
    state = node[stateind]
    blank = node[blankind]
    fvalue = int(node[find])
    cost = int(node[gind])
    path = node[pathind]

    newnode = deepcopy(node)

    if( action == "left"):
        temp = state[blank[0]][blank[1] - 1]
        state[blank[0]][blank[1] - 1] = -1
        state[blank[0]][blank[1]] = temp

        hval = findh(state, dim)
        fval = cost + 1 + int(hval)
        cost = cost + 1
        path += "L,"

        newnode = (fval, state, [blank[0], blank[1] - 1], cost, path)

    if (action == "right"):
        temp = state[blank[0]][blank[1] + 1]
        state[blank[0]][blank[1]+ 1] = -1
        state[blank[0]][blank[1]] = temp

        hval = findh(state, dim)
        fval = cost + 1 + int(hval)
        cost = cost + 1
        path += "R,"

        newnode = (fval, state, [blank[0], blank[1] + 1], cost, path)

    if (action == "up"):
        temp = state[blank[0] - 1][blank[1]]
        state[blank[0] - 1][blank[1]] = -1
        state[blank[0]][blank[1]] = temp

        hval = findh(state, dim)
        fval = cost + 1 + int(hval)
        cost = cost + 1
        path += "U,"

        newnode = (fval, state, [blank[0] - 1, blank[1]], cost, path)

    if (action == "down"):
        temp = state[blank[0] + 1][blank[1]]
        state[blank[0] + 1][blank[1]] = -1
        state[blank[0]][blank[1]] = temp

        hval = findh(state, dim)
        fval = cost + 1 + int(hval)
        cost = cost + 1
        path += "D,"

        newnode = (fval, state, [blank[0] + 1, blank[1]], cost, path)

    return newnode


#find h values based on manattan distance or number of misplace tiles based on value of usenaive
# if usenaive == 1 then return h value as sum of number of misplaced tiles, else sum of manhatttan distances
def findh( arr, dim):
    mandarr = [[0 for x in range(dim)] for y in range(dim)]
    h = 0
    hnaive = 0;
    for i in range( dim ):
        for j in range (dim):
            if (arr[i][j] != -1):
                num = arr[i][j]
                rowf = int((num-1)/dim)
                colf = (num-1) % dim
                mand = abs(i - rowf) + abs( j - colf)
                h+=mand
                if mand != 0 :
                    hnaive += 1
                mandarr[i][j] = mand

    #print (h)
    if usenaive == 1:
        h = hnaive

    return h


#implementation of astar algorithm
def astar( n, inp, out ):
    dim = int(n)
    goalarray = []


    start = [[0 for x in range(dim)] for y in range(dim)]
    i = 0
    j = 0
    blank = [0,0]
    with open(inp) as fp:
        for line in fp:
            j = 0
            numbers = line.split(",")
            for number in numbers:
                if number == '' or number == '\n':
                    start[i][j] = -1
                    blank = [i,j]
                else:
                    #print(number)
                    start[i][j] = int(number)
                j+=1
            i+=1

    h = findh(start, dim)
    explored = []

    q = Q.PriorityQueue()

    startg = 0
    q.put((h, start, blank,startg,""))
    f = open(out, 'w')
    while not q.empty():
        currnode = q.get()
        explored.append(currnode[stateind])
        #f.write(str(currnode[find]))
        #f.write(' ')
        #f.write(str(currnode[stateind]))

        #f.write('\n')
        if goalnodecheck( currnode, dim ) == True :
            outstr = currnode[pathind]
            outstr = outstr[:-1]
            f.write (outstr)
            #print((len(outstr)/2))
            #print(len(explored))
            return

        #left move
        if currnode[blankind][1] != 0:
            tempnode1 = deepcopy( currnode )
            newnode = makenode( tempnode1, "left", dim)
            if not newnode[stateind] in explored:
                q.put(newnode)
        #right move
        if currnode[blankind][1] != (dim - 1):
            tempnode2 = deepcopy(currnode)
            newnode = makenode( tempnode2, "right", dim)
            if not newnode[stateind] in explored:
                q.put(newnode)
        #up move
        if currnode[blankind][0] != 0:
            tempnode3 = deepcopy(currnode)
            newnode = makenode(tempnode3, "up", dim)
            if not newnode[stateind] in explored:
                q.put(newnode)
        #down move
        if currnode[blankind][0] != dim - 1:
            tempnode4 = deepcopy(currnode)
            newnode = makenode(tempnode4, "down", dim)
            if not newnode[stateind] in explored:
                q.put(newnode)






#implementation of id astar algorithm
def idastar( n, inp, out ):
    dim = int(n)
    start = [[0 for x in range(dim)] for y in range(dim)]
    i = 0
    j = 0
    blank = [0, 0]
    with open(inp) as fp:
        for line in fp:
            j = 0
            numbers = line.split(",")
            for number in numbers:
                if number == '' or number == '\n':
                    start[i][j] = -1
                    blank = [i, j]
                else:
                    # print(number)
                    start[i][j] = int(number)
                j += 1
            i += 1

    h = findh(start, dim)
    #print(str(blank))
    node = (h, start, blank, 0, "")
    nextF = 0
    bound = h
    while( 1 ):
        nextF = search(node, bound, dim)
        if nextF == -2:
            return
        #fd.write(str(bound ))
        #fd.write('\n')
        bound = nextF


#recursive search function getting called from id astar
def search( node, bound, dim ):
    #fd.write("%s %s\n" % (str(node[find]), str(node[stateind])) )
    #fd.write('\n')
    fval = node[find]
    if( fval > bound ):
        return fval
    if( goalnodecheck(node, dim )):
        f = open(out, 'w')
        outstr = node[pathind]
        outstr = outstr[:-1]
        f.write(outstr)
        sys.exit()
        #return -2

    minF = 1000000000
    # left move
    if node[blankind][1] != 0:
        tempnode1 = deepcopy(node)
        newnode = makenode(tempnode1, "left", dim)
        minL = search(newnode, bound, dim)
        if( minL < minF ):
            minF = minL

    # right move
    if node[blankind][1] != (dim - 1):
        tempnode2 = deepcopy(node)
        newnode = makenode(tempnode2, "right", dim)
        minR = search(newnode, bound, dim)
        if( minR < minF ):
            minF = minR

    # up move
    if node[blankind][0] != 0:
        tempnode3 = deepcopy(node)
        newnode = makenode(tempnode3, "up", dim)
        minU = search(newnode, bound, dim)
        if( minU < minF ):
            minF = minU

    # down move
    if node[blankind][0] != dim - 1:
        tempnode4 = deepcopy(node)
        newnode = makenode(tempnode4, "down", dim)
        minD = search(newnode, bound, dim)
        if( minD < minF ):
            minF = minD

    return minF





#input----------------
algo = sys.argv[1]
n = sys.argv[2]
inp = sys.argv[3]
out = sys.argv[4]
#fd = open('debug.txt', 'w')
#-------------------

#start_time = time.time()

if algo == "1":
    astar(n, inp, out)
elif algo =="2":
    idastar(n, inp, out)

#print("--- %s seconds ---" % (time.time() - start_time))



