import numpy as np
import networkx as nx

class sbm:
    def __init__(self, partition, av_degree_in, av_degree_out):
        self._partition = partition
        self._clusters = []
        self._d_in = av_degree_in
        self._d_out = av_degree_out

    def create_graph(self):
        n = sum(self._partition)
        k = len(self._partition)
        b = np.array(self._partition)
        index = np.cumsum(b)
        C = [list((index[i - 1] % n) + range(b[i])) for i in range(k)]
        G = nx.Graph()
        G.add_nodes_from(range(n))
        for i in range(k):
            for j in range(k):
                if i == j:
                    for u in C[i]:
                        for v in C[i]:
                            if u < v and np.random.random() < 1. * self._d_in / (len(C[i]) - 1):
                                G.add_edge(u, v, weight = 1)
                else:
                    for u in C[i]:
                        for v in C[j]:
                            if u < v and np.random.random() < 1. * self._d_out * n / (n * n - sum(b * b)):
                                G.add_edge(u, v, weight = 1)
        self._clusters = C
        return G

    def clusters(self):
        return self._clusters

    def clusters_index(self):
        clusters_index = np.zeros(sum(self._partition))
        for i, g in enumerate(self._clusters):
            for u in g:
                clusters_index[u] = i
        return clusters_index

def hierachical_index(i,numbers):
    i_ = []
    for n in numbers:
        i_.append(i % n)
        i = i // n
    return np.array(i_)
    
class hsbm:
    def __init__(self, numbers, parameters):
        self._parameters = parameters
        self._numbers = numbers

    def create_graph(self):
        G = nx.Graph()
        n = np.product(self._numbers)
        intensities = [np.prod(self._parameters[:k + 1]) for k in range(len(self._numbers))]
        for i in range(n):
            i_ = hierachical_index(i,self._numbers)
            for j in range(i):
                j_ = hierachical_index(j,self._numbers)
                k = np.max(np.where(i_ != j_))
                weight = np.random.poisson(intensities[k])
                if weight > 0:
                    G.add_edge(i,j,weight = weight)
        return G

    def pos(self):
        pos = {}
        n = np.product(self._numbers)
        for i in range(n):
            i_ = hierachical_index(i,self._numbers)
            x = np.sqrt(np.random.random()) * np.cos(np.random.random() * 2 * np.pi)
            y = np.sqrt(np.random.random()) * np.sin(np.random.random() * 2 * np.pi)
            fact = 1.
            for k in range(len(self._numbers)):
                fact = 2 * fact
                x += fact * np.cos(i_[k] * 2 * np.pi / self._numbers[k] + np.pi / 4)
                y += fact * np.sin(i_[k] * 2 * np.pi / self._numbers[k] + np.pi / 4)
            pos[i] = np.array([x,y])
        return pos

def score(pred_clustering, true_clustering):
    precision = 0.
    recall = 0.
    f1 = 0.
    total = 0.
    for c in pred_clustering:
        precision_ = 0.
        recall_ = 0.
        f1_ = 0.
        for true_c in true_clustering:
            intersection = len(list(set(c) & set(true_c)))
            if intersection > 0:
                precision_ = max(precision_, 1. * intersection / len(c))
                recall_ = max(recall_, 1. * intersection / len(true_c))
                if precision_ >0 and recall_ > 0:
                    f1_ = max(f1_, 2. / (1. / precision_ + 1. / recall_))
        precision += len(c) * precision_
        recall += len(c) * recall_
        f1 += len(c) * f1_
        total += len(c)
    if total > 0:
        precision = precision / total
        recall = recall / total
        f1 = f1 / total
    return precision, recall, f1
