from utils import *

def analyse():
    G=load_graph()
    n_components=components.number_connected_components(G)
    componentlist = list(components.connected_components(G))

    rankscore=nx.pagerank(G)
    toprank=sorted(list(G.nodes()),key=lambda node:-rankscore[node])
    toprank = toprank[:20]

    cluster=dict()
    for v in G.nodes():
        clusterdict[v] = nx.clustering(G, v)
    nodelist=list(G.nodes())
    clusterlist = sorted(nodelist, key=lambda name: - clusterdict[name])

    centraldict = centrality.betweenness_centrality(G, k=int(0.05 * len(G.nodes())))
    centralist = sorted(nodelist, key=lambda name: - centraldict[name])

    return n_components,toprank,clusterlist,clusterdict,centralist,centraldict
