from utils import *

def get_neighbors(G,person):
    neighbor=dict()
    for nbr in G.neighbors(person):
        neighbor[nbr]=G[person][nbr]['correlation']
    top_neighbor=list(neighbor.keys())
    top_neighbor=sorted(top_neighbor,key=lambda nbr:-neighbor[nbr])
    top_neighbor = top_neighbor[:10]
    for one in top_neighbor:
        print(one)
    return top_neighbor
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("person", help="input a name to query his/her neighbors")
    args = parser.parse_args()
    get_neighbors(load_graph(), args.person)
    