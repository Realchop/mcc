import networkx as nx
import matplotlib.pyplot as plt


type Clique = set[int]

def vote_single(G: nx.Graph, v: int) -> int:
    d_v = G.degree[v]
    if d_v == 0:
        return 1
        
    neighbor_degrees = sorted([G.degree[u] for u in G.neighbors(v)], reverse=True)
    
    max_c = 1
    for i, d_u in enumerate(neighbor_degrees):
        if d_u >= (i + 1):
            max_c = i + 2 
        else:
            break
            
    return min(max_c, d_v + 1)

def vote(G: nx.Graph) -> None:
    for v in G.nodes:
        G.nodes[v]["vote"] = vote_single(G, v)

def plot_graph(G: nx.Graph, seed: int = 0) -> None:
    if len(G.nodes) > 100:
        print("Not doing that. Limit is 100 nodes.")
        return

    plt.figure(figsize=(40, 40))

    pos = nx.spring_layout(G, seed=seed)

    custom_labels = nx.get_node_attributes(G, 'vote')   
    nx.draw(G, pos, with_labels=True, labels=custom_labels, font_size=60, node_size=6000)

def plot_graph_with_clique_cover(G: nx.Graph, clique_cover: list[Clique], seed: int = 0) -> None:
    if len(G.nodes) > 100:
        print("Not doing that. Limit is 100 nodes.")
        return

    coloring_dict = {}

    for color, clique in enumerate(clique_cover):
        for node in clique:
            coloring_dict[node] = color

    color_map = plt.cm.get_cmap('turbo', len(clique_cover))
    
    node_colors = [coloring_dict[node] for node in G.nodes()]

    plt.figure(figsize=(40, 40))

    pos = nx.spring_layout(G, seed=seed) 

    nx.draw(G, pos, node_color=node_colors, with_labels=True, cmap=color_map, font_size=60, node_size=6000)

