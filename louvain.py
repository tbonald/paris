import networkx as nx

def maximize(G,gamma,eps):
    # node weights
    node_weight = {u: 0. for u in G.nodes()}
    for (u,v) in G.edges():
        node_weight[u] += G[u][v]['weight']
        node_weight[v] += G[u][v]['weight']
    # total weight
    wtot = sum(list(node_weight.values()))
    # clusters
    cluster = {u:u for u in G.nodes()}
    # total weight of each cluster
    cluster_weight = {u:node_weight[u] for u in G.nodes()}
    # weights in each community to which the nodes are linked
    w = {u: {v: G[u][v]['weight'] for v in G.neighbors(u) if v != u} for u in G.nodes()}
    increase = True
    while increase:
        increase = False
        for u in G.nodes():
            # Compute delta for every neighbor
            delta = {}
            for k in w[u].keys():
                delta[k] = w[u][k] - gamma * node_weight[u] * cluster_weight[k] / wtot
            # Compute delta for u itself (if not already done)
            k = cluster[u]
            if k not in w[u].keys():
                delta[k] = - gamma * node_weight[u] * cluster_weight[k] / wtot
            # Compare the greatest delta to epsilon
            l = max(delta,key=delta.get)
            if delta[l] - delta[k] > gamma * (node_weight[u] * node_weight[u] / wtot) + eps / wtot:
                increase = True
                cluster[u] = l
                # Update information about neighbors and the community change of u
                cluster_weight[k] -= node_weight[u]
                cluster_weight[l] += node_weight[u]
                for v in G.neighbors(u):
                    if v != u:
                        w[v][k] -= G[u][v]['weight']
                        if w[v][k] == 0:
                            w[v].pop(k)
                        if l not in w[v].keys():
                            w[v][l] = 0
                        w[v][l] += G[u][v]['weight']
    return cluster


def aggregate(G, cluster):
    H = nx.Graph()
    H.add_nodes_from(list(cluster.values()))
    for (u,v) in G.edges():
        if H.has_edge(cluster[u],cluster[v]):
            H[cluster[u]][cluster[v]]['weight'] += G[u][v]['weight']
        else:
            H.add_edge(cluster[u],cluster[v])
            H[cluster[u]][cluster[v]]['weight'] = G[u][v]['weight']
    return H

def get_clustering(cluster_dict):
    cluster_index = []
    cluster_list = []
    for u,k in cluster_dict.items():
        if k not in cluster_index:
            cluster_index.append(k)
            cluster_list.append([u])
        else:
            cluster_list[cluster_index.index(k)].append(u)
    return cluster_list

def louvain(G,resolution = 1,eps = 0.001):
    gamma = resolution
    cluster = maximize(G,gamma,eps)
    n = len(cluster)
    k = len(set(cluster.values()))
    while k < n:
        H = aggregate(G,cluster)
        new_cluster = maximize(H,gamma,eps)
        cluster = {u: new_cluster[cluster[u]] for u in G.nodes()}
        n = k
        k = len(set(cluster.values()))
    return get_clustering(cluster)

