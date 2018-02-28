from os.path import join
import numpy as np
import networkx as nx

def load_weighted_graph(dataset):
    try:
        G = nx.read_weighted_edgelist(join(dataset,"edge.txt"), nodetype=int)
        G.name = dataset
    except:
        G = nx.Graph(name = "Empty graph")
    return G

def unit_weights(G):
    for (u,v) in G.edges():
        G[u][v]['weight'] = 1
    return G

def load_unweighted_graph(dataset):
    try:
        G = nx.read_edgelist(join(dataset,"edge.txt"), nodetype=int)
        G.name = dataset
    except:
        G = nx.Graph(name = "Empty graph")
    return unit_weights(G)

def load_position(dataset):
    pos = {}
    try:
        f = open(join(dataset,"position.txt"), "r")
        u = 0
        for line in f:
            s = line.split()
            pos[u] = (float(s[0]),float(s[1]))
            u += 1
        f.close()
    except:
        pass
    return pos   

def load_name(dataset):
    name = []
    try:
        f = open(join(dataset,"name.txt"), "r")
        for line in f:
            name.append(line[0:-1])
        f.close()
    except:
        pass
    return name   

def load_dataset(data):
    if data == "openstreet":
        G = load_unweighted_graph(data)
        pos = load_position(data)
        name = []
    elif data == "openflights":
        G = load_weighted_graph(data)
        pos = load_position(data)
        name = load_name(data)
    elif data == "wikipedia-school":
        G = load_weighted_graph(data)
        pos = []
        name = load_name(data)
    else:
        G = nx.Graph()
        pos = []
        name = []
    return G, pos, name
