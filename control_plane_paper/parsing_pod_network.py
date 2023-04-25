
import json 

service_pod_rel_f = open("./service_pod_relationship.txt", "r")
service_pod_rel = service_pod_rel_f.readlines()
service_pod_rel_f.close()

ip_service_dict = {}
ip_pod_dict = {}

for line in service_pod_rel:
    rel_list = line.split("|")
    ip_service_dict[rel_list[1]] =  rel_list[0]
    ip_pod_dict[rel_list[5]] = rel_list[4]


pod_net_f = open("pod_networking.txt", "r")
pod_net_list = pod_net_f.readlines()
pod_net_f.close()

pod_parsed = {}




for i in range(0,len(pod_net_list)):
    try:
        if pod_net_list[i].startswith("****"):
            i += 1
            pod_info = pod_net_list[i].strip().split("|")
            
            node_ip = ".".join(pod_info[2].split(".")[0].split("-")[1:])

            pod_parsed[pod_info[0]] = {
                'pod_ip': pod_info[1],
                'node_ip': node_ip,
                'pod_internal_ec2_ip': pod_info[2],
                'listening_ports': [],
                'incomming_connections': [], 
                'pid': [], 
                'connected_service_names': [],
                'connected_pod_names': []
            }

            i=i+3 #skip bs lines

            line = pod_net_list[i]
            while not line.startswith("****") and len(line)>1:
                connection_line = line.strip().split()

                #check if its connected to pod ip append the open port and add the appropriate connection
                if connection_line[5].startswith("LISTEN"):
                    pod_port = connection_line[3].split(":")[-1]
                    if pod_port not in pod_parsed[pod_info[0]]['listening_ports']:
                        pod_parsed[pod_info[0]]['listening_ports'].append(pod_port)  

                elif not connection_line[3].startswith("127"): #ignore local host stuff
                    foreign_ip = connection_line[4]
                    ip_wo_port = foreign_ip.split(":")[0]

                    if foreign_ip.startswith("10.3."): #if service ip lookup service name
                        if ip_wo_port in ip_service_dict.keys():
                            connection_tuple = (connection_line[3], (foreign_ip, ip_service_dict[ip_wo_port])) 
                            if ip_service_dict[ip_wo_port] not in pod_parsed[pod_info[0]]['connected_service_names']:
                                pod_parsed[pod_info[0]]['connected_service_names'].append(ip_service_dict[ip_wo_port])
                        else:
                            connection_tuple = (connection_line[3], (foreign_ip, "no_service_found")) 

                    elif foreign_ip.startswith("10.2."):
                        if ip_wo_port in ip_pod_dict.keys():
                            connection_tuple = (connection_line[3], (foreign_ip, ip_pod_dict[ip_wo_port]))
                            if ip_pod_dict[ip_wo_port] not in pod_parsed[pod_info[0]]['connected_pod_names']:
                                pod_parsed[pod_info[0]]['connected_pod_names'].append(ip_pod_dict[ip_wo_port])
                        else:
                            connection_tuple = connection_tuple + ("no_pod_found", )

                    elif foreign_ip.startswith("10.20."):
                        connection_tuple = (connection_line[3], (foreign_ip, "node"))

                    else:
                        connection_tuple = (connection_line[3], (foreign_ip, "not_found"))

                    connection_tuple = connection_tuple + (connection_line[5], connection_line[6])
                    pod_parsed[pod_info[0]]['outgoing_connections'].append(connection_tuple)
                    if connection_line[6] not in pod_parsed[pod_info[0]]['pid'] and len(connection_line[6])>1:
                        pod_parsed[pod_info[0]]['pid'].append(connection_line[6])



                i += 1
                line = pod_net_list[i]

    except IndexError:
        pass


# json_pod_parsed = json.dumps(pod_parsed, indent = 4)
with open("json_pod_parsed.json", "w") as outfile:
    json.dump(pod_parsed, outfile, indent = 4)



# service_pod_all_info = {}

# for line in service_pod_rel:
#     print(pod_parsed[rel_list[4]])
#     ip_service_dict[rel_list[0]] = pod_parsed[rel_list[4]]


# with open("json_service_pod_parsed.json", "w") as outfile:
#     json.dump(service_pod_all_info, outfile, indent = 4)