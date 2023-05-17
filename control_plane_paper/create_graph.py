import json
import networkx as nx
import matplotlib.pyplot as plt


# load the JSON data
with open('json_pod_parsed.json', 'r') as f:
    data = json.load(f)

# create an empty directed graph
G = nx.DiGraph()



# add nodes to the graph
for key in data.keys():
    G.add_node(key)

# add edges to the graph
for key, value in data.items():
    for dest in value['outgoing_connections']:
        G.add_edge(key, dest[1][1])


pos = nx.kamada_kawai_layout(G)
node_size = 50
edge_width = 0.5

nx.draw_networkx_nodes(G, pos, node_size=node_size)
nx.draw_networkx_edges(G, pos, width=edge_width)

# visualize the graph
plt.axis('off')

plt.savefig("graph.png")