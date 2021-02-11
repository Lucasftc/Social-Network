from utils import *

def get_path_length(G,path,attr='distance'):
    length=0
    if len(path)>1:
        for i in range(len(path)-1):
            try:
                u=path[i]
                v=path[i+1]
                length+=G[u][v][attr]
            except KeyError:
                print((u,v,attr),'attrerror')
    return length

def ksp(G,source,target,K=10):
    try:
        length,path=nx.single_source_dijkstra(G,source,target)
    except nx.NetworkXNoPath:
        print("no path\n")
        return ([],[[]])
    A=[path]
    A_cost=[length]
    B=[]
    B_cost=[]
    used_edge=set()
    for i in range(len(path)-1):
        used_edge.add((path[i],path[i+1]))
    for k in range(K-1):
        rootpath=A[-1]
        for i in range(len(A[-1])-1):
            removed_nodes=[]
            removed_edges=[]
            stray_node=A[-1][i]
            for j in range(i):
                removed_nodes.append(A[-1][j])
            #print("removed nodes",removed_nodes)
            for node in removed_nodes:
                adjlist=list(G.adj[node])
                for adjnode in adjlist:
                    if G.has_edge(node,adjnode):
                        removed_edges.append((node,adjnode,G[node][adjnode]['correlation'],G[node][adjnode]['distance']))
                        G.remove_edge(node,adjnode)
            for (u,v) in used_edge:
                if G.has_edge(u,v) and u==stray_node:
                    removed_edges.append((u,v,G[u][v]['correlation'],G[u][v]['distance']))
                    G.remove_edge(u,v)
            try:
                length,path=nx.single_source_dijkstra(G,stray_node,target)
            except nx.NetworkXNoPath:
                for (u,v,c,d) in removed_edges:
                    G.add_edge(u,v)
                    G[u][v]['weight']=1
                    G[u][v]['correlation']=c
                    G[u][v]['distance']=d
                continue
            for (u,v,c,d) in removed_edges:
                G.add_edge(u,v)
                G[u][v]['weight']=1
                G[u][v]['correlation']=c
                G[u][v]['distance']=d
            #print("stray path",path)
            newpath=A[-1][:i]+path
            #print("contracate path",newpath)
            if newpath not in B:
                B.append(newpath)
                B_cost.append(get_path_length(G,newpath))
        if len(B)==0:
            print("only have %d path"%(len(A)))
            break
        candidateno=B_cost.index(min(B_cost))
        if B[candidateno] not in A:
            candidatepath=B[candidateno]
            A.append(candidatepath)
            A_cost.append(get_path_length(G,candidatepath))
            for i in range(len(candidatepath)-1):
                used_edge.add((candidatepath[i],candidatepath[i+1]))
            #print("candidate path",B[candidateno])
            B.pop(candidateno)
            B_cost.pop(candidateno)
    A = sorted(A, key=lambda path: get_path_length(G, path, 'distance'))
    for path in A:
        for node in path:
            if(node!=path[-1]):
                print(node, end='->')
            else:
                print(node, end='\n')    
    return A

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("source",help="input a person name as departure")
    parser.add_argument("target",help="input a person name as destination")
    args = parser.parse_args()
    ksp(load_graph(), args.source, args.target)
    
    