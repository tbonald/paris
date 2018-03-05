import numpy as np
import networkx as nx
import scipy.sparse as sp
import scipy.cluster.hierarchy as sch

def spectral(G, k = 20):
    # Laplacian matrix
    n = len(list(G.nodes()))
    A = nx.to_scipy_sparse_matrix(G)
    deg = sp.csr_matrix.dot(A, np.ones(n))
    D = sp.diags(deg)
    L = D - A
    
    # Spectral decomposition
    k_ = min(k,n - 1)
    lam,V = sp.linalg.eigsh(L, k_, sigma = -1)
    index = np.argsort(lam)
    lam,V = lam[index], V[:,index]

    # Connected components
    CC = list(nx.connected_components(G))
    K = min(len(CC),k_)
    V[:,0:K] = np.zeros((n,K))
    for l in range(K):
        V[list(CC[l]),l] = 100. * np.ones(len(CC[l]))
        
    return sch.linkage(V, method =  'ward')
