import networkx as nx
import pulp
from common import Clique


def ilp_clique_cover(G: nx.Graph) -> list[Clique]:
    nodes = list(G.nodes())
    n = len(nodes)
    
    problem = pulp.LpProblem("MCC", pulp.LpMinimize)
    
    # cliques[k] = 1 ako je potrebna k-ta klika
    cliques = pulp.LpVariable.dicts("cliques", range(n), cat=pulp.LpBinary)

    # Uzimaj klike redom (da ne bismo proveravali iste slucajeve samo sa razlicito obelezenim klikama)
    for k in range(n - 1):
        problem += cliques[k] >= cliques[k+1]
    
    # in_clique[v][k] = 1 ako je vertex v u kliki k
    in_clique = pulp.LpVariable.dicts("in_clique", (range(n), range(n)), cat=pulp.LpBinary)
    
    # Minimizujemo broj potrebnih klika
    problem += pulp.lpSum([cliques[k] for k in range(n)])
    
    # Svaki cvor moze biti u samo jednoj kliki
    for v1 in range(n):
        problem += pulp.lpSum([in_clique[v1][k] for k in range(n)]) == 1
        
    # Cvor moze biti u kliki samo ako nam je ona dostupna (cliques[k] == 1)
    for v1 in range(n):
        for k in range(n):
            problem += in_clique[v1][k] <= cliques[k]
            
    # Ako v1 i v2 nisu povezani granom onda nisu u istoj kliki
    for v1 in range(n):
        for v2 in range(v1 + 1, n):
            if not G.has_edge(nodes[v1], nodes[v2]):
                for k in range(n):
                    problem += in_clique[v1][k] + in_clique[v2][k] <= 1
                    
    # Max sat vremena 8 niti
    problem.solve(pulp.PULP_CBC_CMD(msg=False, timeLimit=60*60, threads=8))
    
    # Citanje resenja
    out = []
    for k in range(n):
        if pulp.value(cliques[k]) > 0.5:
            current_clique = [nodes[i] for i in range(n) if pulp.value(in_clique[i][k]) > 0.5]
            if current_clique:
                out.append(current_clique)
                
    return out

