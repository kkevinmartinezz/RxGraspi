import rustworkx as rx
import math
from rustworkx import dijkstra_shortest_paths
from rustworkx.visualization import graphviz_draw
import os

os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin'

from rustworkx.visit import BFSVisitor, DijkstraVisitor
from rustworkx.visit import DFSVisitor

class TreeEdgesRecorderDfs(DFSVisitor):

    def __init__(self):
        self.edges = []

    def tree_edge(self, edge):
        self.edges.append(edge)

class TreeEdgesRecorderBfs(BFSVisitor):

    def __init__(self):
        self.edges = []

    def tree_edge(self, edge):
        self.edges.append(edge)

class Node:
  def __init__(self, label, color, x, y, z):
      self.label = label
      # Color of the node depending on 0 or 1
      self.color = color
      # Coordinates of the node
      self.x = x
      self.y = y
      self.z = z

class Edge:
    def __init__(self, node1, node2, weight):
        self.node1 = node1
        self.node2 = node2
        self.weight = weight

def createGraph(filename):
    graph = rx.PyGraph()
    with open(filename, "r") as f:
        lines = f.readlines()
        header = lines[0].split()

        # Dimensions of the graph
        dimX, dimY, dimZ = map(int, header)

        # Stores necessary data for creating edges
        prevLayer = [[None] * dimX for i in range(dimY)]
        currLayer = [[None] * dimX for i in range(dimY)]
        prevRow = [None] * dimX  # Allocates necessary space beforehand
        currRow = [None] * dimX  # Allocates necessary space beforehand
        prevNode = None

        line_idx = 1

        # Graph creation
        for z in range(dimZ):
            for y in range(dimY):
                line = lines[line_idx].strip().split(" ")
                line_idx += 1
                for x in range(dimX):
                    nodeObj = Node((z * dimX * dimY) + (y * dimX) + x, int(line[x]), x, y, z)
                    node = graph.add_node(nodeObj)
                    nodeObj.label = node
                    currRow[x] = node
                    currLayer[y][x] = node

                    # Left of the node
                    if prevNode != None:
                        graph.add_edge(node, prevNode, Edge(nodeObj, graph.get_node_data(prevNode), 1))

                    # Down of the node
                    if prevRow[x] != None:
                        graph.add_edge(node, prevRow[x], Edge(nodeObj, graph.get_node_data(prevRow[x]), 1))

                    if (prevLayer[y][x] != None):
                        graph.add_edge(node, prevLayer[y][x], Edge(nodeObj, graph.get_node_data(prevLayer[y][x]), 1))

                    # Southeast of the node
                    if (x + 1 < dimX) and (prevRow[x + 1] != None):
                        graph.add_edge(node, prevRow[x + 1], Edge(nodeObj, graph.get_node_data(prevRow[x + 1]), math.sqrt(2)))

                    # Southwest of the node
                    if (x - 1 >= 0) and (prevRow[x - 1] != None):
                        graph.add_edge(node, prevRow[x - 1], Edge(nodeObj, graph.get_node_data(prevRow[x - 1]), math.sqrt(2)))

                    # Checks if the node isn't the last node on the line
                    if (x < dimX - 1):
                        prevNode = node
                    else:
                        prevNode = None
                # Stores the previous row as the current row, clears current row
                prevRow, currRow = currRow, [None] * dimX

            prevLayer, currLayer = currLayer, [[None] * dimX for i in range(dimY)]

        add_cathode_node(graph, dimX, dimY, dimZ)
    return graph


def add_cathode_node(g, dimX,dimY,dimZ):
    cathodeObj = Node(g.num_nodes(), 2, 0, 0, 0)
    cathode = g.add_node(cathodeObj)
    currNodes = g.node_indices()
    for z in range(dimZ):
        for x in range(dimX):
            g.add_edge(cathode, currNodes[z * dimX + x], Edge(cathodeObj, g.get_node_data(currNodes[z * dimX + x]), 1))

def node_attr_fn(node):
    attr_dict = {
        "style": "filled",
        "shape": "circle",
        "label": str(node.label),
        "rank": "same"
    }
    # find out how to reach into Node class for color
    # if node is 0 make black, if 1 make white
    if node.color == 2:
        attr_dict["color"] = "blue"
        attr_dict["fillcolor"] = "blue"
        attr_dict["fontcolor"] = "white"
    elif node.color == 0:
        attr_dict["color"] = "black"
        attr_dict["fillcolor"] = "black"
        attr_dict["fontcolor"] = "white"
    elif node.color == 1:
        attr_dict["color"] = "black"
        attr_dict["fillcolor"] = "white"
    return attr_dict

def visualizeGraphGV(g, file):
    graph_dict = {}
    graphviz_draw(g, filename=file, node_attr_fn=node_attr_fn,
                  graph_attr=graph_dict, method ="neato")

def connectedComponents(edge):
    if ((edge.node1.color == 0 and edge.node2.color == 1) or (edge.node1.color == 1 and edge.node2.color == 0)):
        return False
    return True


def filterGraph(g, visualize, filteredImageFile):
    edges = g.filter_edges(connectedComponents)

    edgeList = []
    for edge in edges:
        node1 = g.get_edge_data_by_index(edge).node1.label
        node2 = g.get_edge_data_by_index(edge).node2.label
        edgeList.append( (node1, node2) )

    filteredGraph = g.edge_subgraph(edgeList)
    if visualize:
        visualizeGraphGV(filteredGraph, filteredImageFile)
    return edges

#Uses DFS to traverse graph and print's all edges reachable from source node
def dfs(g, source):
    nodes = []
    nodes.append(source)
    visDFS = TreeEdgesRecorderDfs()
    rx.dfs_search(g, nodes, visDFS)
    print('DFS Edges:', visDFS.edges)

#Uses BFS to traverse graph and print's all edges reachele from source node
def bfs(g, source):
    nodes = []
    nodes.append(source)
    visBFS = TreeEdgesRecorderBfs()
    rx.bfs_search(g, nodes, visBFS)
    print('BFS Edges:', visBFS.edges)

#finds shortest path between the cathode and target node
def shortest_path_from_cathode(g, target):
    cathode = g.num_nodes()-1
    path = dijkstra_shortest_paths(g, cathode, target, weight_fn=None, default_weight=1)
    if len(path) == 0:
        print("No Path Found")
    else:
        print('Shortest Path between', cathode, 'and', target , path)

#finds shortest path between two nodes
def shortest_path_btwn_nodes(g, source, target):
    path = dijkstra_shortest_paths(g, source, target, weight_fn=None, default_weight=1)
    if len(path) == 0:
        print("No Path Found")
    else:
        print('Shortest Path between', source, 'and', target , path)

def shortest_path_all_nodes(g):
    cathode = g.num_nodes() - 1
    all_paths = dijkstra_shortest_paths(g, cathode)
    paths = {}
    for node in all_paths.keys():
        if g.get_node_data(node).color == 0:
            paths[node] = list(all_paths[node])
    return paths

def run_rustworkxKM(type):
    output_file = f"graph/rustworkxKM{type}.png"
    print("Generating Graph...")
    file = "testCases/10x10.txt"
    if type == "graph":
        graph = createGraph(file)
        visualizeGraphGV(graph, output_file)
        return 0
    elif type == "filtered":
        graph = createGraph(file)
        filterGraph(graph, True, output_file)
        return 0
    elif type == "bfs":
        graph = createGraph(file)
        filterGraph(graph, False, output_file)
        paths = shortest_path_all_nodes(graph)
        # print(paths)
        return paths



# Defining main function
def main():
    run_rustworkxKM("graph")
    run_rustworkxKM("filtered")
    run_rustworkxKM("bfs")

if __name__=="__main__":
    main()