import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import dendrogram

plt.rcParams.update({'font.size': 14})
    
def plot_results(range_, nb_blocks_, results, xlabel, filename = ""):
    algos = ["Paris","Louvain","Spectral"]
    colors = ['b','r','g']
    markers = ['o','^','+']
    
    # Precision, recall, F1
    ylabel = ["Precision", "Recall", "F1 score"]
    metric = ["prec","recall","f1"]
    for j in range(len(metric)): 
        plt.figure(figsize = (8,5))
        plt.xlim(0.5, max(range_) * 1.05)
        plt.ylim(0, 1.05)
        for i, algo in enumerate(algos):
            mean_ = np.array([results[i][k][j] for k in range(len(range_))])
            std_ = np.array([results[i][k][j + len(algos)] for k in range(len(range_))])
            plt.plot(range_, mean_, marker = markers[i], color = colors[i], label = algo)
            plt.fill_between(range_, mean_ - std_, mean_ + std_, facecolor = colors[i], interpolate = True, alpha = .1)
        plt.xlabel(xlabel)
        plt.ylabel(ylabel[j])
        plt.legend()
        if filename != "":
            plt.savefig(filename + "-" + metric[j] + ".pdf", bbox_inches = 'tight')
        else:
            plt.show()

    # Number of clusters        
    plt.figure(figsize = (8,5))    
    ymax = 0.
    ymin = 0.
    for i, algo in enumerate(algos):
        mean_ = np.array([results[i][k][2 * len(metric)] for k in range(len(range_))])
        std_ = np.array([results[i][k][2 * len(metric) + 1] for k in range(len(range_))])
        ymin = min(ymin, np.min(mean_ - std_))
        ymax = max(ymax, np.max(mean_ + std_))
        plt.plot(range_, mean_, marker = markers[i], color = colors[i], label = algo)
        plt.fill_between(range_, mean_ - std_, mean_ + std_, facecolor = colors[i], interpolate = True, alpha = .1)
    plt.plot(range_, nb_blocks_, '--', color = 'k')
    plt.xlim(0.5, max(range_) * 1.05)
    plt.ylim(max(ymin * 0.95, 0), ymax * 1.05)
    plt.xlabel(xlabel)
    plt.ylabel("Number of clusters")
    plt.legend()
    if filename != "":
        plt.savefig(filename + "-nb.pdf", bbox_inches = 'tight')
    else:
        plt.show()

def plot_resolution(resolutions_paris, resolutions_louvain, nb_clusters_louvain, key_resolutions_louvain, filename = ""):
    plt.figure(figsize = (8,5))
    plt.ylim(ymin=0, ymax=len(resolutions_paris))
    plt.xlabel('Resolution')
    plt.ylabel('Number of clusters')
    plt.step(list(reversed(resolutions_paris)), range(len(resolutions_paris)), 'r')
    plt.xscale('log')
    for r in resolutions_paris:
        plt.axvline(x = r, color='k', alpha=.2)
    if filename != "":
        plt.savefig(filename + "-paris.pdf", bbox_inches = 'tight')
    else:
        plt.show()

    plt.figure(figsize = (8,5))
    plt.ylim(ymin=0, ymax=len(resolutions_paris))
    plt.xlabel('Resolution')
    plt.ylabel('Number of clusters')
    plt.plot(resolutions_louvain,nb_clusters_louvain, 'r+')
    for r in key_resolutions_louvain:
        if r < resolutions_paris[1]:
            plt.axvline(x = r, color='k', alpha=.2)
    plt.xscale('log')
    if filename != "":
        plt.savefig(filename + "-louvain.pdf", bbox_inches = 'tight')
    else:
        plt.show()
    
def plot_clustering(G, C, pos, width = 16, height = 8, filename = ""):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.5','0.3','0.8', '0.6','0.2','0.7','0.1','0.9']
    plt.figure(figsize = (width, height))
    length = [len(c) for c in C]
    index = np.argsort(-np.array(length))
    plt.axis('off')
    draw_nodes = nx.draw_networkx_nodes(G, pos, node_size=50, node_color='w')
    draw_nodes.set_edgecolor('k')
    nx.draw_networkx_edges(G, pos, alpha=.1)
    for l in range(min(len(C),len(colors))):
        draw_nodes = nx.draw_networkx_nodes(G, pos, node_size=50, nodelist = C[index[l]],node_color=colors[l])
        draw_nodes.set_edgecolor('k')
    if filename != "":
        plt.savefig(filename + ".pdf", bbox_inches = 'tight')
    else:
        plt.show()
        
def plot_clusterings(G, C_list, pos, width = 16, height = 8, filename = ""):
    k = len(C_list)
    nrows = k // 2 + k % 2
    ncols = 2
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k', '0.5','0.3','0.8', '0.6','0.2','0.7','0.1','0.9']
    plt.figure(figsize = (width * ncols, height * nrows))
    for k_ in range(k):
        C = C_list[k_]
        length = [len(c) for c in C]
        index = np.argsort(-np.array(length))
        if filename == "":
            plt.subplot(nrows, ncols, k_ + 1) 
            plt.title("Rank " + str(k_ + 1) + " (" + str(len(C)) + " clusters)")
        else:
            plt.figure(figsize = (width, height))
        plt.axis('off')
        draw_nodes = nx.draw_networkx_nodes(G, pos, node_size=50, node_color='w')
        draw_nodes.set_edgecolor('k')
        nx.draw_networkx_edges(G, pos, alpha=.05)
        for l in range(min(len(C),len(colors))):
            draw_nodes = nx.draw_networkx_nodes(G, pos, node_size=50, nodelist = C[index[l]],node_color=colors[l])
            draw_nodes.set_edgecolor('k')
        if filename != "":
            plt.savefig(filename + str(k_) + ".pdf", bbox_inches = 'tight')
    if filename == "":
        plt.show()

def plot_dendrogram(D, logscale="True", filename = ""):
    plt.figure(figsize=(25, 10))
    Dlog = D.copy()
    if logscale:
        Dlog[:,2] = np.log(D[:,2]) - np.log(D[0,2])
    dendrogram(Dlog, leaf_rotation=90.)
    plt.axis('off')
    if filename != "":
        plt.savefig(filename + ".pdf", bbox_inches = 'tight')
    else:
        plt.show()
