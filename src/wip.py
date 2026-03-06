import networkx as nx
from common import vote

# 2min 27s 
def find_k_clique_bitparallel(G: nx.Graph, k: int) -> list[int] | None:
    core_nodes = [n for n, d in G.degree() if d >= k - 1]
    if len(core_nodes) < k:
        return None
    
    H = G.subgraph(core_nodes)
    nodes = list(H.nodes())
    n = len(nodes)
    
    node_to_idx = {node: i for i, node in enumerate(nodes)}
    adj_bits = [0] * n
    for i, u in enumerate(nodes):
        for neighbor in H.neighbors(u):
            if neighbor in node_to_idx:
                adj_bits[i] |= (1 << node_to_idx[neighbor])

    def backtrack(candidates_bitset, current_clique):
        if len(current_clique) == k:
            return current_clique
        
        if bin(candidates_bitset).count('1') + len(current_clique) < k:
            return None

        temp_candidates = candidates_bitset
        while temp_candidates:
            u_idx = (temp_candidates & -temp_candidates).bit_length() - 1
            
            temp_candidates &= ~(1 << u_idx)
            
            new_candidates = candidates_bitset & adj_bits[u_idx]
            
            res = backtrack(new_candidates & ~((1 << (u_idx + 1)) - 1), 
                            current_clique + [nodes[u_idx]])
            
            if res:
                return res
        return None

    full_bitset = (1 << n) - 1
    return backtrack(full_bitset, [])

def minimum_clique_cover(G: nx.Graph) -> list[int]:
    clique_id_counter = 0

    cliques = []
    
    vote(G)
    
    while any(G.nodes[n].get("clique") is None for n in G.nodes):
        votes = nx.get_node_attributes(G, "vote")
        
        active_unlabeled_votes = [ v for n, v in votes.items() if v > 1 and G.nodes[n].get("clique") is None ]
        
        if not active_unlabeled_votes:
            for node in G.nodes:
                if G.nodes[node].get("clique") is None:
                    G.nodes[node]["clique"] = clique_id_counter
                    clique_id_counter += 1
            break

        target_v = max(active_unlabeled_votes)
            
        candidates = [ 
            n for n, v in votes.items() 
            if v == target_v and G.nodes[n].get("clique") is None ]
        candidates.sort(key=lambda n: G.degree(n))
        
        for u in candidates:
            if G.nodes[u].get("clique") is not None:
                continue
                
            valid_neighbors = [
                v for v in G.neighbors(u) 
                if G.nodes[v]["vote"] >= target_v
            ]
            
            target_k = target_v - 1
            
            if len(valid_neighbors) >= target_k:
                res = find_k_clique_bitparallel(G.subgraph(valid_neighbors), target_k)
                
                if res is not None:
                    res.append(u)
                    for node in res:
                        G.nodes[node]["clique"] = clique_id_counter
                        if not G.nodes[node].get("clique_ctr"):
                            G.nodes[node]["clique_ctr"] = 0
                        G.nodes[node]["clique_ctr"] += 1
                    
                    clique_id_counter += 1
                    break 
            
            G.nodes[u]["vote"] -= 1

    # TODO: Extract cover
    return cliques

