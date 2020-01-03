import sys
import networkx as nx
import numpy as nd
import collections

class Path:
    def __init__(self, row, col):
        self.row = row
        self.col = col

    def __eq__(self, other):
        return self.row == other.row and self.col == other.col

    def __hash__(self):
        return hash((self.row, self.col))

# Debug output
def print_maze(maze):
    for i in range(0, maze.shape[0]):
        for j in range(0, maze.shape[1]):
            print(maze[i,j], end='')
        print('')

# Parse input
def read_maze():
    row = 0
    col = 0
    maze = nd.empty((117,115), dtype='object')
    for line in sys.stdin:
        for c in line:
            if c != '\n':
                maze[row, col] = c 
            col += 1
        row += 1
        col = 0

    return maze

# Helper
def letter(maze,row,col):
    return maze[row, col] not in ['#','.', ' ']

# Helper
def path(maze, row, col):
    return maze[row, col] == '.'

# Extract coordinates of all warp points
def find_warps(maze):
    warps = {}
    nrows = maze.shape[0]
    ncols = maze.shape[1]
    # Skip the edges to avoid index failures
    for r in range(1, nrows-1):
        for c in range(1, ncols-1):
            if letter(maze,r,c):
                if path(maze,r-1,c):
                    warps[(r-1,c)] = "{}{}".format(maze[r,c], maze[r+1,c])
                elif path(maze,r+1,c):
                    warps[(r+1,c)] = "{}{}".format(maze[r-1,c], maze[r,c])
                elif path(maze,r,c-1):
                    warps[(r,c-1)] = "{}{}".format(maze[r,c], maze[r,c+1])
                elif path(maze,r,c+1):
                    warps[(r,c+1)] = "{}{}".format(maze[r,c-1], maze[r,c])
    return warps

# Build graph from array-based maze format
def build_graph(maze, warps):
    graph = nx.Graph()
    nrows = maze.shape[0]
    ncols = maze.shape[1]
    # Skip the edges to avoid index failures
    for r in range(1, nrows-1):
        for c in range(1, ncols-1):
            if path(maze,r,c):
                if path(maze,r-1,c) and not graph.has_edge((r,c),(r-1,c)):
                    graph.add_edge((r,c), (r-1,c))
                if path(maze,r+1,c) and not graph.has_edge((r,c),(r+1,c)):
                    graph.add_edge((r,c), (r+1,c))
                if path(maze,r,c-1) and not graph.has_edge((r,c),(r,c-1)):
                    graph.add_edge((r,c), (r,c-1))
                if path(maze,r,c+1) and not graph.has_edge((r,c),(r,c+1)):
                    graph.add_edge((r,c), (r,c+1))
    
    warp_points = collections.defaultdict(list)

    for pos in warps.keys():
        name = warps[pos]
        warp_points[name].append(pos)
    
    start = None
    end = None
    for name in warp_points.keys():
        if len(warp_points[name]) > 1:
            v0 = warp_points[name][0]
            v1 = warp_points[name][1]
            graph.add_edge(v0, v1)
        elif name == 'AA':
            start = warp_points[name][0]
        elif name == 'ZZ':
            end = warp_points[name][0]

    print('shortest path: ', nx.shortest_path_length(graph, start, end))

    return graph

maze = read_maze()
warps = find_warps(maze)
graph = build_graph(maze, warps)

# Debug
for (r,c) in warps.keys():
    maze[r,c] = 'o'



# create undirected graph with networkx library
# graph.add_edge(a, b, weight=1)
# print(nx.shortest_path(graph, 'YOU', 'SAN', weight='weight'))
# print("Part 2: the shortest path is {}".format(nx.shortest_path_length(graph, 'YOU', 'SAN', weight='weight') - 2))