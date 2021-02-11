import numpy as np
import pandas as pd
import networkx as nx
import json
from networkx.readwrite import json_graph
from networkx.algorithms import centrality
from networkx.algorithms.shortest_paths import generic
from networkx.algorithms import components
from networkx.algorithms import smallworld
from networkx.algorithms.link_analysis.pagerank_alg import pagerank
import matplotlib.pyplot as plt
import argparse

from config import Config

def load_graph(path=Config.graph_path):
    with open(path,mode='r',encoding='utf-8') as fgraph:
        G=nx.Graph()
        G = json_graph.node_link_graph(json.load(fgraph))
    return G

def load_basic():
    with open(Config.namelist_path,mode='r',encoding='utf-8') as fname:
        namelist=json.load(fname)
    with open(Config.orglist_path,mode='r',encoding='utf-8') as forg:
        orglist=json.load(forg)
    with open(Config.placelist_path,mode='r',encoding='utf-8') as fplace:
        placelist = json.load(fplace)
    return namelist,orglist,placelist

