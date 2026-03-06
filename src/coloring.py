from typing import Literal
import networkx as nx
from collections import defaultdict
from typing import Literal
from common import vote


def greedy_color(G: nx.Graph, strategy: Literal["greedy", "vote"]) -> dict:
    if strategy == "vote":
        vote(G)
        ordered_nodes = sorted(
            G.nodes(),
            key=lambda n: (G.nodes[n]["vote"], -G.degree(n)),
            reverse=True
        )
    else:
        ordered_nodes = sorted(
            G.nodes(),
            key=lambda n: G.degree(n),
            reverse=True
        )
    
    coloring = {}
    
    for node in ordered_nodes:
        neighbor_colors = {
            coloring[neighbor] 
            for neighbor in G.neighbors(node) 
            if neighbor in coloring
        }
        
        assigned_color = 0
        while assigned_color in neighbor_colors:
            assigned_color += 1
            
        coloring[node] = assigned_color
        
    return coloring

def minimum_clique_cover(G: nx.Graph, strategy: Literal["greedy", "vote"]):
    G_bar = nx.complement(G)
    
    coloring = greedy_color(G_bar, strategy)
    
    cliques_by_color = defaultdict(list)
    for vertex, color in coloring.items():
        cliques_by_color[color].append(vertex)
        
    return list(cliques_by_color.values())
