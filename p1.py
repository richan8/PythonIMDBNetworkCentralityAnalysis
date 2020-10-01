'''
MODULES USED:
urllib
json
networkx
matplotlib
unidecode
'''

saveFile='db3.json'
import json
import networkx as nx
import matplotlib.pyplot as plt
from unidecode import unidecode


G=nx.Graph()

nodeList=[]
edgeList=[]
unconnectedEdgeList=[]

with open(saveFile,'r') as f:
        data=json.loads(f.read())

for movie in data['Movies']:
    for x in movie['actors']:
        x=unidecode(x).strip(' ')
        if((x not in nodeList) and (x!='N/A')):
            nodeList.append(x)
        for y in movie['actors']:
            y=unidecode(y).strip(' ')
            if((y not in nodeList) and (y!='N/A')):
                nodeList.append(y)
            if((x!=y) and (x!='N/A') and (y!='N/A') and ((x,y) not in edgeList) and ((y,x) not in nodeList)):
                edgeList.append((x,y))

for x in nodeList:
    for y in nodeList:
        if(x!=y and ((x,y) not in edgeList)):
            unconnectedEdgeList.append((x,y))

pos=nx.spring_layout(G)

G.add_nodes_from(nodeList)
G.add_edges_from(edgeList)

pos=nx.spring_layout(G)

plt.figure('The Network of Co-Actors')
nx.draw(G,pos,node_color='r',node_size=130,alpha=0.8,font_size=10,edge_color='b',width=3,with_labels=True,label='The Network of Hollywood Actors')
plt.show()

#############KATZ CENTRALITY
c=nx.katz_centrality(G)
cc=sorted(c.items(), key=lambda x: x[1],reverse=True)
barGraphLimit=10
x=[]
y=[]
for item in cc[:barGraphLimit]:
    x.append(item[0])
    y.append(item[1])
    
plt.figure('Katz Centrality')
plt.bar(x,y,color='b')
plt.title('Katz Centrality: Top 10 Actors')
plt.show()

cc=sorted(c.items(), key=lambda x: x[0])
y=[]
for item in cc:
    y.append(item[1])
    
plt.figure('How Katz Centrality varies')
plt.plot(y)
plt.title('How the Katz Centrality Varies amongst actors')
plt.show()

nodeCol=[]
for x in c.items():
    nodeCol.append(x[1]*2*x[1])

plt.figure('Katz Centrality: Visualization') 
plt.title('Katz Centrality: Visualization\nBlue->Yellow is Less to more ')
nx.draw(G,pos,node_color=nodeCol,node_size=130,alpha=0.9,font_size=10,edge_color='b',width=3,with_labels=True,label='Suggested Connections - Jackard Coeffecient')
plt.show()

#############CLOSENESS CENTRALITY
c=nx.closeness_centrality(G,wf_improved=True, reverse=True)
cc=sorted(c.items(), key=lambda x: x[1],reverse=True)
barGraphLimit=10
x=[]
y=[]
for item in cc[:barGraphLimit]:
    x.append(item[0])
    y.append(item[1])
    
plt.figure('Closeness Centrality')
plt.bar(x,y,color='b')
plt.title('Closeness Centrality: Top 10 Actors')
plt.show()

cc=sorted(c.items(), key=lambda x: x[0])
y=[]
for item in cc:
    y.append(item[1])
    
plt.figure('How Closeness Centrality varies')
plt.plot(y)
plt.title('How the Closeness Centrality Varies amongst actors')
plt.show()


nodeCol=[]
for x in c.items():
    nodeCol.append(x[1]*2*x[1])

plt.figure('Closeness Centrality: Visualization') 
plt.title('Closeness Centrality: Visualization\nBlue->Yellow is Less to more ')
nx.draw(G,pos,node_color=nodeCol,node_size=130,alpha=0.9,font_size=10,edge_color='b',width=3,with_labels=True,label='Suggested Connections - Jackard Coeffecient')
plt.show()
#############BETWEENNESS CENTRALITY
c=nx.betweenness_centrality(G)
cc=sorted(c.items(), key=lambda x: x[1],reverse=True)
barGraphLimit=10
x=[]
y=[]
for item in cc[:barGraphLimit]:
    x.append(item[0])
    y.append(item[1])

plt.figure('Top 10 Ranking for actors based on Betweeness Centrality')
plt.bar(x,y,color='r')
plt.title('Betweenness Centrality: Top 10 Actors')
plt.show()

nodeCol=[]
for x in c.items():
    nodeCol.append(x[1]*2)

plt.figure('Betweenness Centrality: Visualization') 
plt.title('Betweenness Centrality: Visualization\nBlue->Yellow is Less to more ')
nx.draw(G,pos,node_color=nodeCol,node_size=130,alpha=0.9,font_size=10,edge_color='b',width=3,with_labels=True,label='Suggested Connections - Jackard Coeffecient')
plt.show()

cc=sorted(c.items(), key=lambda x: x[0])
y=[]
for item in cc:
    y.append(item[1])



plt.figure('How Betweenness Centrality Varies')
plt.plot(y,color='r')
plt.title('How the Betweenness Centrality varies amongst actors')
plt.show()

#############PREDICTING FUTURE POSSIBLE CO-ACTORS BY LINK PREDICTION OF THEIR NETWORK

#############UNCONNECTED EDGES i.e. POSSIBLE NEW LINKS
'''
for edge in unconnectedEdgeList:
    print(edge)
print('\nLUnconnected Edges-> %s'%(len(unconnectedEdgeList)))
'''
print('\nTotal Possible New Connections -> %s'%(len(unconnectedEdgeList)))

#############JACKARD COEFFECIENT
jc=[]
for edge in unconnectedEdgeList:
    x=sorted(nx.jaccard_coefficient(G,[edge]))
    if((x[0] not in jc) and ((x[0][1],x[0][0],x[0][2]) not in jc)):
        jc.append(x[0])

jc.sort(key=lambda x: x[2],reverse=True)
jcEdgeList=[]
edgeColors=[]
for x in jc:
    #((x[0],x[1]) not in jcEdgeList) and ((x[1],x[0] not in jcEdgeList))):
    if(x[2]>0.2):
        jcEdgeList.append((x[0],x[1]))
        edgeColors.append(x[2]*2)

x=[]
y=[]
for item in jc[:barGraphLimit]:
    x.append('%s\n%s'%(item[0],item[1]))
    y.append(item[2])

plt.figure('Top Possible Predicted Actor Connections - Jackard Coeffecient')
plt.bar(x,y,color='g')
plt.title('Top Possible Predicted Actor Connections - Jackard Coeffecient')
plt.show()


plt.figure('Possible New Connections - Jackard Coeffecient') 
plt.title('Possible New Connections (Dasehed Lines)\n Blue->Yellow is weaker to Stronger')
nx.draw(G,pos,node_color='r',node_size=130,alpha=0.69,font_size=10,edge_color='b',width=3,with_labels=True,label='Suggested Connections - Jackard Coeffecient')
nx.draw_networkx_edges(G,pos,edgelist=jcEdgeList,edge_color=edgeColors,width=4,alpha=1,style='dashed')
plt.show()

#############RESOURCE ALLOCATION INDEX
jc=[]
for edge in unconnectedEdgeList:
    x=sorted(nx.resource_allocation_index(G,[edge]))
    if((x[0] not in jc) and ((x[0][1],x[0][0],x[0][2]) not in jc)):
        jc.append(x[0])

jc.sort(key=lambda x: x[2],reverse=True)

jcEdgeList=[]
edgeColors=[]
for x in jc:
    if(x[2]>0.2):
        jcEdgeList.append((x[0],x[1]))
        edgeColors.append(x[2]*2)

x=[]
y=[]
for item in jc[:barGraphLimit]:
    x.append('%s\n%s'%(item[0],item[1]))
    y.append(item[2])

plt.figure('Top Possible Predicted Actor Connections - RAI')
plt.bar(x,y,color='g')
plt.title('Top Possible Predicted Actor Connections - RAI')
plt.show()


plt.figure('Possible New Connections - RAI') 
plt.title('Possible New Connections - RAI (Dashed Lines)\n Blue->Yellow is weaker to Stronger')
nx.draw(G,pos,node_color='r',node_size=130,alpha=0.69,font_size=10,edge_color='b',width=3,with_labels=True,label='Suggested Connections - Jackard Coeffecient')
nx.draw_networkx_edges(G,pos,edgelist=jcEdgeList,edge_color=edgeColors,width=4,alpha=1,style='dashed')
plt.show()