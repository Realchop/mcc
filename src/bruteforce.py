import networkx as nx
from common import Clique

# Implementacija koja se NE koristi jer je prespora i za najmanje primere
def minimum_clique_cover(G: nx.Graph) -> list[Clique]:
    # Idemo po cvorovima sa najvecim stepenima
    nodes = sorted(list(G.nodes()), key=lambda x: G.degree(x), reverse=True)
    
    best_cover = []
    # Svi su svoja klika
    best_k = len(nodes) + 1 

    def backtrack(idx, current_cover):
        nonlocal best_cover, best_k

        # Vec smo uzeli vise
        if len(current_cover) >= best_k:
            return

        # Sve cvorove smo pokrili
        if idx == len(nodes):
            if len(current_cover) < best_k:
                best_k = len(current_cover)
                best_cover = [clique.copy() for clique in current_cover]
            return

        v = nodes[idx]

        # Probaj da dodas u postojecu kliku
        for clique in current_cover:
            if all(G.has_edge(v, u) for u in clique):
                clique.append(v)
                backtrack(idx + 1, current_cover)
                clique.pop() 

        # Dodaj u novu
        current_cover.append([v])
        backtrack(idx + 1, current_cover)
        current_cover.pop() 

    backtrack(0, [])
    return best_cover

