
import json 

pods_processes_f = open("./pods_processes.txt", "r")
pods_processes_list = pods_processes_f.readlines()
pods_processes_f.close()

process_pod_dict = {}

for i in range(0, len(pods_processes_list)): 
    try:
        if pods_processes_list[i].startswith("****"):
            process_line = pods_processes_list[i]
            while(not process_line.startswith("Java Services running on Pod")):
                i+=1
                process_line = pods_processes_list[i]
            
            pod_name = pods_processes_list[i].split(":")[1].strip(" ")

            process_pod_dict[pod_name] = {} #list of tuples (process, processname)

            i += 1 

            if not pods_processes_list[i].startswith("bash: jps: command not found"):
                count = 0
                while(not pods_processes_list[i].startswith("****")):
                    process_pod_dict[pod_name][pods_processes_list[i].split()[0]] = pods_processes_list[i].split()[1]
                    count+=1
                    i+=1
                if count == 1:
                    # print(pod_name)
                    while(not pods_processes_list[i].startswith(pod_name)):
                        i=i-1 #backtracking lines of the file
                    
                    i+=2 #skipping header columns line

                    while(not pods_processes_list[i].startswith("Java Services running on Pod")):
                        split_process_line = pods_processes_list[i].split()[:13]
                        process_id = split_process_line[1]
                        process_name = " ".join(split_process_line[10:])
                        process_pod_dict[pod_name][process_id] = process_name
                        i=i+1
                    
                    



            else:
                while(not pods_processes_list[i].startswith(pod_name)):
                    i=i-1 #backtracking lines of the file
                
                i+=2 #skipping header columns line

                while(not pods_processes_list[i].startswith("Java Services running on Pod")):
                    split_process_line = pods_processes_list[i].split()[:13]
                    process_id = split_process_line[1]
                    process_name = " ".join(split_process_line[10:])
                    # if not process_name.startswith("bash -c ps") and not process_name.startswith("ps -aux"):
                    process_pod_dict[pod_name][process_id] = process_name
                    i=i+1

    except IndexError:
        pass

with open("json_pod_parsed.json", "w") as outfile:
    json.dump(process_pod_dict, outfile, indent = 4)
