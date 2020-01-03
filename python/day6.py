import sys
import networkx as nx

class Obj:
    name = None
    in_orbit_around = None

    def __init__(self, name):
        self.name = name

    def nOrbits(self):
        return 1 + self.in_orbit_around.nOrbits() if self.in_orbit_around != None else 0    

objects = {} # For part 1 I rolled my own graph
graph = nx.Graph() # For part 2, it was easier to use networkx

for line in sys.stdin:
    # Read nodes
    names = line.split(')')
    a = names[0].strip()
    b = names[1].strip()

    # create undirected graph with networkx library
    graph.add_edge(a, b, weight=1)

    # create my own tree for part 1
    if not a in objects:
        objects[a] = Obj(a)
    if not b in objects:
        objects[b] = Obj(b)
    objectA = objects[a]
    objectB = objects[b]
    objectB.in_orbit_around = objectA

# Part 1

checksum = 0
for name in objects.keys():
    obj = objects[name]
    checksum += obj.nOrbits()

print("Part 1: there are {} direct and indirect orbits".format(checksum))

# Part 2

print(nx.shortest_path(graph, 'YOU', 'SAN', weight='weight'))

print("Part 2: the shortest path is {}".format(nx.shortest_path_length(graph, 'YOU', 'SAN', weight='weight') - 2))