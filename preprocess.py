from utils import *
import thulac

def entity_recognize():
    data = pd.read_csv(Config.news_path, delimiter='\t')
    thu=thulac.thulac()
    titles=data['title']
    texts=data['text']
    namelist=[]
    placelist=[]
    orglist=[]
    for i in range(len(data)):
        if i % 1000 ==0:
            print("processed %d pieces of news"%i)
        namelist.append([])
        placelist.append([])
        orglist.append([])
        words=thu.cut(str(titles[i])+str(texts[i]))
        for word in words:
            if word[1]=='np':
                namelist[i].append(word[0])
            if word[1]=='ns':
                placelist[i].append(word[0])
            if word[1]=='ni':
                orglist[i].append(word[0])

    with open(Config.namelist_path,mode='w',encoding='utf-8') as fname:
        json.dump(namelist,fname,ensure_ascii=False,indent=2)

    with open(Config.placelist_path,mode='w',encoding='utf-8') as fplace:
        json.dump(placelist,fplace,ensure_ascii=False,indent=2)

    with open(Config.orglist_path,mode='w',encoding='utf-8') as forg:
        json.dump(orglist, forg, ensure_ascii=False, indent=2)

def count_frequency():
    namelist, orglist, placelist = load_basic()
    orgcount=dict()
    placecount=dict()
    namecount=dict()
    for i in range(len(orglist)):
        unique_org=list(set(orglist[i]))
        for j in range(len(unique_org)):
            if unique_org[j] not in orgcount.keys():
                orgcount[unique_org[j]]=1
            else:
                orgcount[unique_org[j]]+=1
    keys=list(orgcount.keys())
    for key in keys:
        if len(key)<=1:
            orgcount.pop(key)
    for i in range(len(placelist)):
        unique_place=list(set(placelist[i]))
        for j in range(len(unique_place)):
            if(unique_place[j]) not in placecount.keys():
                placecount[unique_place[j]]=1
            else:
                placecount[unique_place[j]]+=1
    keys=list(placecount.keys())
    for key in keys:
        if len(key)<=1:
            placecount.pop(key)
    for i in range(len(namelist)):
        unique_name=list(set(namelist[i]))
        for j in range(len(unique_name)):
            if unique_name[j] not in namecount.keys():
                namecount[unique_name[j]]=1
            else:
                namecount[unique_name[j]]+=1
    keys=list(namecount.keys())
    for key in keys:
        if len(key)<=1:
            namecount.pop(key)
    if ' ' in namecount.keys():
        namecount.pop(' ')

    sorted_name=sorted(namecount.items(),key=lambda item:-item[1])
    sorted_place=sorted(placecount.items(),key=lambda item:-item[1])
    sorted_org = sorted(orgcount.items(), key=lambda item: - item[1])
    return namecount,sorted_name,sorted_place,sorted_org

def generate_graph(namecount):
    G = nx.Graph()
    namelist,_,__=load_basic()
    alpha=[chr(i) for i in list(range(65,91))+list(range(97,123))]
    for line_name in namelist:
        unique_name=list(set(line_name))
        for i in range(len(unique_name)):
            for j in range(i+1,len(unique_name)):
                namei=unique_name[i]
                namej=unique_name[j]
                if (len(namei)>1) and (len(namej)>1) and (namei.isalpha()) and (namej.isalpha()) and (namei[0] not in alpha) and (namej[0] not in alpha):
                    if (namei,namej) not in G.edges:
                        G.add_edge(namei,namej,correlation=1)
                        G.edges[namei,namej]['weight']=1
                    elif (namei,namej) in G.edges:
                        G.edges[namei,namej]['correlation']+=1
    for u,v in G.edges:
        try:
            G.edges[u,v]['distance']=1-(G.edges[u,v]['correlation'])/(namecount[u]+namecount[v]-G.edges[u,v]['correlation'])
        except:
            print("%s,%d,%s,%d,%d" % (u, namecount[u], v, namecount[v], G.edges[u, v]['correlation']))

    with open(Config.graph_path,mode='w',encoding='utf-8') as fgraph:
        json.dump(json_graph.node_link_data(G), fgraph, ensure_ascii=False, indent=2)
        
if __name__ == "__main__":
    entity_recognize()
    namecount, sorted_name, sorted_place, sorted_org = count_frequency()
    generate_graph(namecount)
            
    