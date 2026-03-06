from typing import Literal
import networkx as nx
from common import Clique, vote


def find_clique_of_size_k(G: nx.Graph, k: int):
    if k <= 0: 
        return None

    nodes = list(G.nodes())

    def backtrack(remaining_nodes: list[int], current_clique: list[int]):
        if len(current_clique) == k:
            return current_clique

        if len(current_clique) + len(remaining_nodes) < k:
            return None
        
        for i, node in enumerate(remaining_nodes):
            if all(G.has_edge(node, c) for c in current_clique):
                res = backtrack(remaining_nodes[i+1:], current_clique + [node])
                if res is not None:
                    return res
        return None

    return backtrack(nodes, [])

def minimum_clique_cover(G: nx.Graph, strategy: Literal["biggest", "smallest"] = "biggest") -> list[Clique]:
    clique_cover = []

    update_votes = True
    
    while G.number_of_nodes() > 0:
        if update_votes:
            vote(G)
            update_votes = False

        votes = nx.get_node_attributes(G, 'vote')
        
        active_votes = [v for v in votes.values() if v > 1]
        
        if not active_votes:
            for node in list(G.nodes()):
                clique_cover.append([node])
                G.remove_node(node)
            break

        if strategy == 'biggest':
            degree_target = max(active_votes)
        else: 
            degree_target = min(active_votes)
            
        candidates = [n for n, v in votes.items() if v == degree_target]

        candidates.sort(key=lambda n: G.degree(n))
        
        for u in candidates:
            valid_neighbors = [ v for v in G.neighbors(u) if G.nodes[v]['vote'] >= degree_target ]
            
            k = degree_target - 1
            
            if len(valid_neighbors) >= k:
                clique = find_clique_of_size_k(G.subgraph(valid_neighbors), k)
                
                if clique is not None:
                    clique.append(u)
                    clique_cover.append(clique)
                    G.remove_nodes_from(clique)
                    update_votes = True
                    break 
            
            G.nodes[u]['vote'] -= 1
        
    return clique_cover
