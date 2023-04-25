pod_cap_file = open("pod_cap.output", "r")

pod_bound_dict = {}
prevline = ""
count = 0 

which_cap = "CapAmb:"


for line in pod_cap_file:
    line = line.strip()
    if line.startswith("Pod Name"): 
        count += 1
        pod_name = line.split(":")[1]
        pod_name = pod_name.strip()

        
    if prevline.startswith(which_cap):
        pods_caps_str = line.split("=")[1]
        pods_caps_list = pods_caps_str.split(",")
        pod_bound_dict[pod_name] = pods_caps_list

    prevline = line 


first_pod_bound = list(pod_bound_dict.values())[0]
first_pod_bound_set = set(first_pod_bound)


pod_bound_extras = {}
for pod_name,pods_caps_list in pod_bound_dict.items():
    pods_caps_set = set(pods_caps_list)
    # print(pod_name, pods_caps_set)
    extra_caps = pods_caps_set.difference(first_pod_bound_set)
    # print(extra_caps)
    if len(extra_caps) > 0:
        pod_bound_extras[pod_name] = list(extra_caps)

print(which_cap,pod_bound_extras)


