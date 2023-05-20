import json
import networkx as nx
import matplotlib.pyplot as plt



def create_nodes_list(data):
    nodes_to_ingest =  []
    for node in data.keys():
        node_with_attr_tuple = (node , data[node])
        nodes_to_ingest.append(node_with_attr_tuple)
    return nodes_to_ingest


def create_edges_list(data):
    edges_to_ingest = []
    for node_key, node_values in data.items():
        for connection in node_values['incomming_connections']:
            if connection[0].startswith('10.2.152.169') or connection[1][0].startswith('10.2.152.169'):
                if connection[1][0].startswith('10.2.'):
                    edge_attrs = {'sending' : connection[1][0].split(':')[1],
                                'listening' : connection[0].split(':')[1] 
                                }
                    edge_tuple = (connection[1][1], node_key, edge_attrs)
                    edges_to_ingest.append(edge_tuple)
                
                #print(connection[1][1], node_key, 'sending:', connection[1][0].split(':')[1], 'listening:', connection[0].split(':')[1])
    return edges_to_ingest



if __name__ == '__main__':
    G = nx.DiGraph()
    json_file = 'json_pod_parsed.json'
    with open(json_file) as json_file:
        data = json.load(json_file)
    nodes_to_ingest = create_nodes_list(data)
    edges_to_ingest = create_edges_list(data)
    G.add_nodes_from(nodes_to_ingest)
    # print(edges_to_ingest)
    G.add_edges_from(edges_to_ingest)
    # print(G.edges())
    # nx.draw(G, with_labels=True)
    # plt.show()
    
    for node in G.nodes():
        # Convert node attributes to compatible types
        attributes = G.nodes[node]
        for attr, value in attributes.items():
            if isinstance(value, (int, float)):
                attributes[attr] = str(value)
            elif isinstance(value, dict) or isinstance(value, list):
                attributes[attr] = json.dumps(value)

    for edge in G.edges():
        # Convert edge attributes to compatible types
        start_node, end_node = edge
        attributes = G.edges[start_node, end_node]
        for attr, value in attributes.items():
            if isinstance(value, (int, float)):
                attributes[attr] = str(value)
            elif isinstance(value, dict) or isinstance(value, list):
                attributes[attr] = json.dumps(value)

    # nx.write_graphml(G, "auth_node.graphml")



