# 6.00.2x Problem Set 5
# Graph optimization
# Finding shortest paths through MIT buildings
#

import string
import sys
# This imports everything from `graph.py` as if it was defined in this file!
from graph import * 

#
# Problem 2: Building up the Campus Map
#
# Before you write any code, write a couple of sentences here 
# describing how you will model this problem as a graph. 

# This is a helpful exercise to help you organize your
# thoughts before you tackle a big design problem!
#

def load_map(mapFilename):
    """ 
    Parses the map file and constructs a directed graph

    Parameters: 
        mapFilename : name of the map file

    Assumes:
        Each entry in the map file consists of the following four positive 
        integers, separated by a blank space:
            From To TotalDistance DistanceOutdoors
        e.g.
            32 76 54 23
        This entry would become an edge from 32 to 76.

    Returns:
        a directed graph representing the map
    """
    # TODO
    print "Loading map from file..."
    g = WeightedDigraph()
    
    handle = open(mapFilename, 'r')
    
    for line in handle :
        strings = line.split()
        src = Node(strings[0])
        dest = Node(strings[1])
        edge = WeightedEdge(src, dest, float(strings[2]), float(strings[3]))
        if not g.hasNode(src) :
            g.addNode(src)
        if not g.hasNode(dest) :
            g.addNode(dest)
        try :
            g.addEdge(edge)
        except ValueError, errMessage :
            print errMessage
    return g
#
# Problem 3: Finding the Shortest Path using Brute Force Search
#
# State the optimization problem as a function to minimize
# and what the constraints are
#

def DFS(graph, start, end, path = [], totalDist=0, outdoorDist=0, found_paths = []):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    #print 'Current dfs path:', printPath(path)
    if start == end:
        return path, totalDist, outdoorDist
    for edge in graph.edgesOf(start):
        
        if edge[0] not in path: #avoid cycles  
            totalDist += edge[1][0]
            outdoorDist += edge[1][1]
            try :
                newPath, newTotalDist, newOutdoorDist = DFS(graph,edge[0],end,path,totalDist,outdoorDist,found_paths)
            except :
                #The DFS could not find the path and just return a "None" object that can't
                # be used to initialized three variables
                newPath = None
            totalDist -= edge[1][0]
            outdoorDist -= edge[1][1]
            if newPath != None:
                found_paths.append((newPath,newTotalDist,newOutdoorDist))

def bruteForceSearch(digraph, start, end, maxTotalDist, maxDistOutdoors):    
    """
    Finds the shortest path from start to end using brute-force approach.
    The total distance travelled on the path must not exceed maxTotalDist, and
    the distance spent outdoor on this path must not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO

    f_p = []
    print "DFS for all possible path"
    DFS(digraph, Node(start), Node(end), found_paths = f_p)
    
    shortest = None
    min_dist = sys.maxint

    for p in f_p :
        if p[2]<=maxDistOutdoors :
            if p[1]<=maxTotalDist :
                if p[1]<min_dist :
                    shortest = p[0]
                    min_dist = p[1]
    if shortest != None :
        return [str(s) for s in shortest]
    else :
        raise ValueError
        
# Test for DFS
"""
nodes = []
for name in range(6):
    nodes.append(Node(str(name)))
g = WeightedDigraph()
for n in nodes:
    g.addNode(n)
g.addEdge(WeightedEdge(nodes[0],nodes[1],2,1))
g.addEdge(WeightedEdge(nodes[1],nodes[2],2,1))
g.addEdge(WeightedEdge(nodes[2],nodes[3],2,1))
g.addEdge(WeightedEdge(nodes[2],nodes[4],2,1))
g.addEdge(WeightedEdge(nodes[3],nodes[4],2,1))
g.addEdge(WeightedEdge(nodes[3],nodes[5],2,1))
g.addEdge(WeightedEdge(nodes[0],nodes[2],2,1))
g.addEdge(WeightedEdge(nodes[1],nodes[0],2,1))
g.addEdge(WeightedEdge(nodes[3],nodes[1],2,1))
g.addEdge(WeightedEdge(nodes[4],nodes[0],2,1))
f_p = []
DFS(g, nodes[0], nodes[5], found_paths=f_p)
print f_p
"""

# Test for problem 3
"""
mit_map = load_map("mit_map.txt")
s = bruteForceSearch(mit_map, '32', '36', maxTotalDist=1000, maxDistOutdoors=1000)
print s
"""

#
# Problem 4: Finding the Shorest Path using Optimized Search Method
#
def shortestDFS(graph, start, end, path = [], shortestPath=None, shortestDist=sys.maxint, maxTotalDist=sys.maxint,\
    maxDistOutdoors=sys.maxint, totalDist=0, outdoorDist=0):
    #assumes graph is a Digraph
    #assumes start and end are nodes in graph
    path = path + [start]
    if start == end:
        return path, totalDist
    for edge in graph.edgesOf(start):
        if edge[0] not in path: #avoid cycles  
            totalDist += edge[1][0]
            outdoorDist += edge[1][1]
            try :
                newPath = None
                if totalDist <= maxTotalDist and outdoorDist <= maxDistOutdoors : 
                    if totalDist < shortestDist :
                        newPath, newTotalDist = shortestDFS(graph,edge[0],end,path, shortestPath, shortestDist,\
                            maxTotalDist, maxDistOutdoors, totalDist, outdoorDist)             
            except :
                #The DFS could not find the path and just return a "None" object that can't
                # be used to initialized three variables
                #newPath = None
                #totalDist -= edge[1][0]
                #outdoorDist -= edge[1][1]
                pass
                
            if newPath != None:
                #print newPath, shortestPath, shortestDist
                shortestPath = newPath
                shortestDist = newTotalDist  
            totalDist -= edge[1][0]
            outdoorDist -= edge[1][1]
    return shortestPath, shortestDist

                
def directedDFS(digraph, start, end, maxTotalDist, maxDistOutdoors):
    """
    Finds the shortest path from start to end using directed depth-first.
    search approach. The total distance travelled on the path must not
    exceed maxTotalDist, and the distance spent outdoor on this path must
	not exceed maxDistOutdoors.

    Parameters: 
        digraph: instance of class Digraph or its subclass
        start, end: start & end building numbers (strings)
        maxTotalDist : maximum total distance on a path (integer)
        maxDistOutdoors: maximum distance spent outdoors on a path (integer)

    Assumes:
        start and end are numbers for existing buildings in graph

    Returns:
        The shortest-path from start to end, represented by 
        a list of building numbers (in strings), [n_1, n_2, ..., n_k], 
        where there exists an edge from n_i to n_(i+1) in digraph, 
        for all 1 <= i < k.

        If there exists no path that satisfies maxTotalDist and
        maxDistOutdoors constraints, then raises a ValueError.
    """
    #TODO
    print "Doing directed DFS..."
    shortestPath, shortestDist = shortestDFS(digraph, Node(start), Node(end), maxTotalDist=maxTotalDist, maxDistOutdoors=maxDistOutdoors)
    if shortestPath != None : 
        return [str(s) for s in shortestPath]
    else :
        raise ValueError
        
# Test for directed DFS   
"""
nodes = []
for name in range(6):
    nodes.append(Node(str(name)))
g = WeightedDigraph()
for n in nodes:
    g.addNode(n)
g.addEdge(WeightedEdge(nodes[0],nodes[1],2,1))
g.addEdge(WeightedEdge(nodes[1],nodes[2],2,1))
g.addEdge(WeightedEdge(nodes[2],nodes[3],2,1))
#g.addEdge(WeightedEdge(nodes[2],nodes[4],2,1))
g.addEdge(WeightedEdge(nodes[3],nodes[4],2,1))
g.addEdge(WeightedEdge(nodes[3],nodes[5],2,1))
g.addEdge(WeightedEdge(nodes[0],nodes[2],2,1))
#g.addEdge(WeightedEdge(nodes[1],nodes[0],2,1))
#g.addEdge(WeightedEdge(nodes[3],nodes[1],2,1))
#g.addEdge(WeightedEdge(nodes[4],nodes[0],2,1))
s, d_s = shortestDFS(g, nodes[0], nodes[5])
print s, d_s
"""

# Test for problem 4
"""
mit_map = load_map("mit_map.txt")
s = directedDFS(mit_map, '32', '36', maxTotalDist=1000, maxDistOutdoors=1000)
print s
"""

# Uncomment below when ready to test
#### NOTE! These tests may take a few minutes to run!! ####

if __name__ == '__main__':
    #Test cases
    mitMap = load_map("mit_map.txt")
    print isinstance(mitMap, Digraph)
    print isinstance(mitMap, WeightedDigraph)
    print 'nodes', mitMap.nodes
    print 'edges', mitMap.edges


    LARGE_DIST = 1000000

#      Test case 1
    print "---------------"
    print "Test case 1:"
    print "Find the shortest-path from Building 32 to 56"
    expectedPath1 = ['32', '56']
    brutePath1 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    dfsPath1 = directedDFS(mitMap, '32', '56', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath1
    print "Brute-force: ", brutePath1
    print "DFS: ", dfsPath1
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath1 == brutePath1, expectedPath1 == dfsPath1)

#     Test case 2
    print "---------------"
    print "Test case 2:"
    print "Find the shortest-path from Building 32 to 56 without going outdoors"
    expectedPath2 = ['32', '36', '26', '16', '56']
    brutePath2 = bruteForceSearch(mitMap, '32', '56', LARGE_DIST, 0)
    dfsPath2 = directedDFS(mitMap, '32', '56', LARGE_DIST, 0)
    print "Expected: ", expectedPath2
    print "Brute-force: ", brutePath2
    print "DFS: ", dfsPath2
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath2 == brutePath2, expectedPath2 == dfsPath2)

#     Test case 3
    print "---------------"
    print "Test case 3:"
    print "Find the shortest-path from Building 2 to 9"
    expectedPath3 = ['2', '3', '7', '9']
    brutePath3 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    dfsPath3 = directedDFS(mitMap, '2', '9', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath3
    print "Brute-force: ", brutePath3
    print "DFS: ", dfsPath3
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath3 == brutePath3, expectedPath3 == dfsPath3)

#     Test case 4
    print "---------------"
    print "Test case 4:"
    print "Find the shortest-path from Building 2 to 9 without going outdoors"
    expectedPath4 = ['2', '4', '10', '13', '9']
    brutePath4 = bruteForceSearch(mitMap, '2', '9', LARGE_DIST, 0)
    dfsPath4 = directedDFS(mitMap, '2', '9', LARGE_DIST, 0)
    print "Expected: ", expectedPath4
    print "Brute-force: ", brutePath4
    print "DFS: ", dfsPath4
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath4 == brutePath4, expectedPath4 == dfsPath4)

#     Test case 5
    print "---------------"
    print "Test case 5:"
    print "Find the shortest-path from Building 1 to 32"
    expectedPath5 = ['1', '4', '12', '32']
    brutePath5 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    dfsPath5 = directedDFS(mitMap, '1', '32', LARGE_DIST, LARGE_DIST)
    print "Expected: ", expectedPath5
    print "Brute-force: ", brutePath5
    print "DFS: ", dfsPath5
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath5 == brutePath5, expectedPath5 == dfsPath5)

#     Test case 6
    print "---------------"
    print "Test case 6:"
    print "Find the shortest-path from Building 1 to 32 without going outdoors"
    expectedPath6 = ['1', '3', '10', '4', '12', '24', '34', '36', '32']
    brutePath6 = bruteForceSearch(mitMap, '1', '32', LARGE_DIST, 0)
    dfsPath6 = directedDFS(mitMap, '1', '32', LARGE_DIST, 0)
    print "Expected: ", expectedPath6
    print "Brute-force: ", brutePath6
    print "DFS: ", dfsPath6
    print "Correct? BFS: {0}; DFS: {1}".format(expectedPath6 == brutePath6, expectedPath6 == dfsPath6)

#     Test case 7
    print "---------------"
    print "Test case 7:"
    print "Find the shortest-path from Building 8 to 50 without going outdoors"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        bruteRaisedErr = 'Yes'
  
    try:
        directedDFS(mitMap, '8', '50', LARGE_DIST, 0)
    except ValueError:
        dfsRaisedErr = 'Yes'
  
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

#     Test case 8
    print "---------------"
    print "Test case 8:"
    print "Find the shortest-path from Building 10 to 32 without walking"
    print "more than 100 meters in total"
    bruteRaisedErr = 'No'
    dfsRaisedErr = 'No'
    try:
        bruteForceSearch(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        bruteRaisedErr = 'Yes'
    
    try:
        directedDFS(mitMap, '10', '32', 100, LARGE_DIST)
    except ValueError:
        dfsRaisedErr = 'Yes'
  
    print "Expected: No such path! Should throw a value error."
    print "Did brute force search raise an error?", bruteRaisedErr
    print "Did DFS search raise an error?", dfsRaisedErr

