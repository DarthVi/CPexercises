from collections import namedtuple
from os import path
from json import load
from ortools.constraint_solver import pywrapcp
import matplotlib.pyplot as plt
from matplotlib.pyplot import subplots
from matplotlib.patches import Rectangle
from matplotlib.collections import PatchCollection
from matplotlib import cm
from numpy import linspace


def load_instance(instance):
    edges = []
    n_nodes = 0 
    with open(instance) as file:
        for line in file.readlines():
            line_data = line.split()
            if line_data[0] == 'e':
                edge = (int(line_data[1]), int(line_data[2]),)
                if max(edge) > n_nodes:
                    n_nodes = max(edge) 
                edges.append(edge)
    return n_nodes, edges

def graph_visualization(nodes, collector, edges):
    adjacency_matrix = [ [0] * len(nodes) for _ in range(len(nodes))]
    for node_1, node_2 in edges:
        adjacency_matrix[node_1 - 1][node_2 - 1] = 1
        
    assert(collector.SolutionCount() > 0), 'There is no solution. Nothing to visualize'
    for m in range(collector.SolutionCount()):
        import networkx as nx
        import matplotlib.pyplot as plt
        G = nx.Graph()
        
        node_color = {}
        for i, node in enumerate(nodes):
            p = adjacency_matrix[i]
            c = collector.Solution(m).Value(node)
                       
            if sum(p) > 0:
                for tmp_node in [j for j, v in enumerate(p) if v]:
                    G.add_edge(i + 1, tmp_node + 1)
                    
            #===================================================================
            # Trivial nodes 
            # else:
            #     G.add_node(i + 1)
            #===================================================================
                if not(c in node_color):
                    node_color[c] = [] 
                node_color[c].append(i + 1)
        positions = nx.spring_layout(G)
        plt.subplot(111)
        for c, node_idxs in node_color.items():
            nx.draw_networkx_nodes(G, {node: positions[node] for node in node_idxs}, nodelist=node_idxs, node_color=None)
        nx.draw_networkx_edges(G, positions)  # , width=1.0, alpha=0.5)
        nx.draw_networkx_labels(G, positions, {i:str(i) for i in positions})  # , font_size=16)
        plt.show()
