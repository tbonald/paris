import numpy as np
import networkx as nx

# for data export only
import csv

from hierarchy import top_clustering
from paris import paris 
from louvain import louvain
from spectral import spectral
from synthetic_data import sbm, score

algos = ["paris", "louvain", "spectral"]

def clustering(G, algo):
    nodes = list(G.nodes())
    if algo == "paris":
        D = paris(G)
        C = top_clustering(D, nodes)
    elif algo == "louvain":
        C = louvain(G)
    elif algo == "spectral":
        D = spectral(G)
        C = top_clustering(D, nodes)
    return C

def get_results(nb_samples, nb_blocks = 40, block_size = [10], d_int = 5, d_ext = 1):
    sbm_model = sbm(nb_blocks * block_size, d_int, d_ext)  
    score_samples = [[],[],[]]
    nb_clusters_samples = [[],[],[]]
    for s in range(nb_samples):
        G = sbm_model.create_graph()
        true_clustering = sbm_model.clusters()
        CC = list(nx.connected_components(G))
        for l in range(len(CC) - 1):
            i = np.random.choice(list(CC[l]))
            j = np.random.choice(list(CC[l + 1]))
            G.add_edge(i, j, weight = 1)
        for i, algo in enumerate(algos):
            pred_clustering = clustering(G, algo)       
            score_samples[i].append(score(pred_clustering, true_clustering))
            nb_clusters_samples[i].append(len(pred_clustering))      
    results = []
    for i in range(len(algos)):
        result = list(np.mean(np.array(score_samples[i]), axis = 0))
        result += list(np.std(np.array(score_samples[i]), axis = 0))
        result += [np.mean(nb_clusters_samples[i]), np.std(nb_clusters_samples[i])]
        results.append(result)
    return results

def get_results_algo(results_):
    results = []
    for i, algo in enumerate(algos):
        result = []
        for k in range(len(results_)):
            result += [results_[k][i]]
        results += [result]
    return results

def save_results(results, filename):
    for i, result in enumerate(results):
        with open(filename + "-" + algos[i] + ".csv", "w") as f:
            writer = csv.writer(f)
            writer.writerows(result)

def experiment_nb(nb_samples, range_, filename = ""):
    results_ = []
    for nb_blocks in range_:
        print(nb_blocks)
        results_.append(get_results(nb_samples, nb_blocks))
    results = get_results_algo(results_)
    if filename != "":
        save_results(results, filename)
    return results

def experiment_deg(nb_samples, range_, filename = ""):
    results_ = []
    for d_ext in range_:
        print(d_ext)
        results_.append(get_results(nb_samples, d_ext = d_ext))
    results = get_results_algo(results_)
    if filename != "":
        save_results(results, filename)
    return results

def experiment_het(nb_samples, range_, block_size, filename = ""):
    results_ = []
    filename = "het"
    for nb_blocks in range_:
        print(nb_blocks)
        results_.append(get_results(nb_samples, nb_blocks, block_size))
    results = get_results_algo(results_)
    if filename != "":
        save_results(results, filename)
    return results
