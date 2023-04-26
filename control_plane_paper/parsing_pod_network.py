
import json 
from parsing_pod_processes import process_pod_dict

if __name__ == '__main__':
    service_pod_rel_f = open("./service_pod_relationship.txt", "r")
    service_pod_rel = service_pod_rel_f.readlines()
    service_pod_rel_f.close()

    ip_service_dict = {}
    ip_pod_dict = {}
    ec2_node_ip_pod_dict = {}


    for line in service_pod_rel[1:]: #ignoring first line as it has column names

        rel_list = line.split("|")
        ip_service_dict[rel_list[1]] =  rel_list[0]
        ip_pod_dict[rel_list[5]] = rel_list[4]
        ec2_node_ip = ".".join(rel_list[6].split("-")[1].split(".")[:4])
        ec2_node_ip_pod_dict[ec2_node_ip] = rel_list[4]


    pod_net_f = open("pod_networking.txt", "r")
    pod_net_list = pod_net_f.readlines()
    pod_net_f.close()

    pod_parsed = {}


    for i in range(0,len(pod_net_list)):
        try:
            if pod_net_list[i].startswith("****"):
                i += 1
                pod_info = pod_net_list[i].strip().split("|")
                
                node_ip = ".".join(pod_info[2].split(".")[0].split("-")[1:]) #this is an annoying diff representation for no fucking good reason lol

                pod_parsed[pod_info[0]] = {
                    'pod_ip': pod_info[1],
                    'node_ip': node_ip,
                    'listening_ports': [],
                    'ougoing_ports' : [],
                    'incomming_connections': [], 
                    'incomming_connected_service_names': [],
                    'incomming_connected_pod_names': [],
                    'outgoing_connections': [], 
                    'outgoing_connected_service_names': [],
                    'outgoing_connected_pod_names': [],
                    'pid': []
                }

                i=i+3 #skip bs lines

                line = pod_net_list[i]
                while not line.startswith("****") and len(line)>1:
                    connection_line = line.strip().split()
                    pod_port = connection_line[3].split(":")[-1]


                    
                    if connection_line[6] not in pod_parsed[pod_info[0]]['pid'] and len(connection_line[6])>1:
                            print(connection_line[6])


                    #Setting incomming and outgoing ports list

                    if connection_line[5].startswith("LISTEN"):
                        if pod_port not in pod_parsed[pod_info[0]]['listening_ports']:
                            pod_parsed[pod_info[0]]['listening_ports'].append(pod_port)  

                    elif connection_line[5].startswith("WAIT") or connection_line[5].startswith("ESTABLISHED"):
                        if pod_port not in pod_parsed[pod_info[0]]['ougoing_ports']:
                            pod_parsed[pod_info[0]]['ougoing_ports'].append(pod_port)  


                    #figuring out incoming and outgoing connections

                    if not connection_line[3].startswith("127") and not connection_line[5].startswith("LISTEN"):
                        if pod_port in pod_parsed[pod_info[0]]['listening_ports']:  #incomming connection
                        #ignore local host stuff and check if listening port. I can do this because all the listening ports are listed first in netstat output
                        
                            foreign_ip = connection_line[4]
                            ip_wo_port = foreign_ip.split(":")[0]

                            #should probably put this if else into a function tbh 
                            if foreign_ip.startswith("10.3."): #if service ip lookup service name
                                if ip_wo_port in ip_service_dict.keys():
                                    connection_tuple = (connection_line[3], (foreign_ip, ip_service_dict[ip_wo_port])) 
                                    if ip_service_dict[ip_wo_port] not in pod_parsed[pod_info[0]]['incomming_connected_service_names']:
                                        pod_parsed[pod_info[0]]['incomming_connected_service_names'].append(ip_service_dict[ip_wo_port])
                                else:
                                    connection_tuple = (connection_line[3], (foreign_ip, "no_service_found")) 

                            elif foreign_ip.startswith("10.2."):
                                if ip_wo_port in ip_pod_dict.keys():
                                    connection_tuple = (connection_line[3], (foreign_ip, ip_pod_dict[ip_wo_port]))
                                    if ip_pod_dict[ip_wo_port] not in pod_parsed[pod_info[0]]['incomming_connected_pod_names']:
                                        pod_parsed[pod_info[0]]['incomming_connected_pod_names'].append(ip_pod_dict[ip_wo_port])
                                else:
                                    connection_tuple = connection_tuple + ("no_pod_found", )

                            elif foreign_ip.startswith("10.20."):
                                if foreign_ip.startswith(node_ip):
                                    connection_tuple = (connection_line[3], (foreign_ip, "same_node"))
                                elif node_ip in ec2_node_ip_pod_dict.keys(): #usally if never reaches this point 
                                    connection_tuple = (connection_line[3], (foreign_ip, ec2_node_ip_pod_dict[node_ip]))
                                else: #usally if never reaches this point 
                                    connection_tuple = (connection_line[3], (foreign_ip, "external_node"))
                            else:
                                connection_tuple = (connection_line[3], (foreign_ip, "not_found"))

                            connection_tuple = connection_tuple + (connection_line[5], connection_line[6])
                            pod_parsed[pod_info[0]]['incomming_connections'].append(connection_tuple)

                        else: 

                            #for outgoing connections (just copy pasted, def should make it a function or a class)
                            foreign_ip = connection_line[4]
                            ip_wo_port = foreign_ip.split(":")[0]

                            #should probably put this if else into a function tbh 
                            if foreign_ip.startswith("10.3."): #if service ip lookup service name
                                if ip_wo_port in ip_service_dict.keys():
                                    connection_tuple = (connection_line[3], (foreign_ip, ip_service_dict[ip_wo_port])) 
                                    if ip_service_dict[ip_wo_port] not in pod_parsed[pod_info[0]]['outgoing_connected_service_names']:
                                        pod_parsed[pod_info[0]]['outgoing_connected_service_names'].append(ip_service_dict[ip_wo_port])
                                else:
                                    connection_tuple = (connection_line[3], (foreign_ip, "no_service_found")) 

                            elif foreign_ip.startswith("10.2."):
                                if ip_wo_port in ip_pod_dict.keys():
                                    connection_tuple = (connection_line[3], (foreign_ip, ip_pod_dict[ip_wo_port]))
                                    if ip_pod_dict[ip_wo_port] not in pod_parsed[pod_info[0]]['outgoing_connected_pod_names']:
                                        pod_parsed[pod_info[0]]['outgoing_connected_pod_names'].append(ip_pod_dict[ip_wo_port])
                                else:
                                    connection_tuple = connection_tuple + ("no_pod_found", )

                            elif foreign_ip.startswith("10.20."):
                                if foreign_ip.startswith(node_ip):
                                    connection_tuple = (connection_line[3], (foreign_ip, "same_node"))
                                elif node_ip in ec2_node_ip_pod_dict.keys(): #usally if never reaches this point 
                                    connection_tuple = (connection_line[3], (foreign_ip, ec2_node_ip_pod_dict[node_ip]))
                                else: #usally if never reaches this point 
                                    connection_tuple = (connection_line[3], (foreign_ip, "external_node"))
                            else:
                                connection_tuple = (connection_line[3], (foreign_ip, "not_found"))

                            connection_tuple = connection_tuple + (connection_line[5], connection_line[6])
                            pod_parsed[pod_info[0]]['outgoing_connections'].append(connection_tuple)
                        



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