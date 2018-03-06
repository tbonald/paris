import numpy as np

# Clustering extraction from a dendrogram

class cluster_tree:
    def __init__(self, node, height, gap, max_gap):
        self.left = None
        self.right = None
        self.node = node
        self.height = height
        self.gap = gap
        self.max_gap = max_gap

def select_clustering(D, nodes, k):
    n = np.shape(D)[0] + 1
    k = min(k,n - 1)
    cluster = {i:[i] for i in range(n)}
    for t in range(k):
        cluster[n + t] = cluster.pop(int(D[t][0])) + cluster.pop(int(D[t][1]))
    clusters = [[nodes[i] for i in c] for c in list(cluster.values())]
    dist = np.sqrt(D[k - 1,2] * D[k,2]) 
    return clusters, dist

def top_clustering(D, nodes):
    clustering, cut = top_cut_clustering(D, nodes)
    return clustering

def top_clusterings(D, nodes, k = 2):
    clusterings = []
    cut = []
    for l in range(k):
        clustering, new_cut = top_cut_clustering(D, nodes, exclude = cut)
        cut += new_cut
        clusterings.append(clustering)
    return clusterings

def top_cut_clustering(D, nodes, exclude = []):
    n = np.shape(D)[0] + 1
    cluster_trees = {i: cluster_tree(i, 0., 0., True) for i in range(n)}
    for t in range(n - 1):
        i = int(D[t][0])
        j = int(D[t][1])
        left_tree = cluster_trees.pop(i)
        right_tree = cluster_trees.pop(j)
        height = np.log(D[t,2]) - np.log(D[0,2])
        if min(i,j) < n and height < float('inf'):
            new_tree = cluster_tree(n + t, height, 0, True)            
        else:
            if left_tree.height < float('inf'):
                left_gap = height - left_tree.height
                if left_gap < left_tree.gap:
                    left_gap = left_tree.gap
                else:
                    if left_tree.node in exclude:
                        left_gap = float('inf')
                    else:
                        left_tree.max_gap = True
            else:
                left_gap = float('inf')
            if right_tree.height < float('inf'):
                right_gap = height - right_tree.height
                if right_gap < right_tree.gap:
                    right_gap = right_tree.gap
                else:
                    if right_tree.node in exclude:
                        right_gap = float('inf') 
                    else:
                        right_tree.max_gap = True
            else:
                right_gap = float('inf')
            new_tree = cluster_tree(n + t, height, min(left_gap, right_gap), False)
        new_tree.left = left_tree
        new_tree.right = right_tree
        cluster_trees[n + t] = new_tree
    tree = list(cluster_trees.values())[0]
    cut = get_cluster_indices(tree)
    return get_clustering(D, nodes, cut), cut

def get_cluster_indices(tree):
    if tree.max_gap:
        return [tree.node]
    else:
        return get_cluster_indices(tree.left) + get_cluster_indices(tree.right)

def get_clustering(D, nodes, cut):
    n = np.shape(D)[0] + 1
    cluster_list = [[i] for i in cut if i < n]
    cluster = {i:[i] for i in range(n)}
    for t in range(n - 1):
        cluster[n + t] = cluster.pop(int(D[t][0])) + cluster.pop(int(D[t][1]))
        if n + t in cut:
            cluster_list.append(cluster[n + t])
    clusters = [[nodes[i] for i in c] for c in cluster_list]
    return clusters

