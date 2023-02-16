from pyvis.network import Network
import os
import sys
import json

net = Network()

# Get the current working directory and build the path for teh json file
cwd = os.getcwd()
path = f"{cwd}/{sys.argv[1]}"


def read_file(name_file):
    with open(f'{name_file}', 'r') as file:
        # Read the contents of the file
        data1 = file.read()
        data = json.loads(data1, strict=False)

    file.close()
    return data


def remove_speacial_char(special_string):
    special_characters = ['@', '#', '$', '*', '&', '\\n', '}']
    normal_string = special_string
    for i in special_characters:
        # Replace the special character with an empty string
        normal_string = normal_string.replace(i, "")
        # Print the string after the removal of special characters
    return normal_string


def vip2nodes(vips, pools, nodes, string, items, label_string):
    # vip --> pool
    for item in items:
        if (string == item['name']):
            pools = pools + 1
            label1 = item['name']
            label2 = item['loadBalancingMode']
            label3 = f"{label1} \n {label2}"
            net.add_node(pools, label=label3, color='#3da831')
            members = item['members']
            net.add_edge(vips, pools, label=label_string)

            # pool --> nodes
            for member in members:
                nodes = nodes + 1
                label1 = member['name']
                net.add_node(nodes, label=label1, color='#9a31a8')
                net.add_edges([(pools, nodes, 2)])
    return pools, nodes        


# add pools,nodes and vips
def add_obj():
    nodes = 0
    pools = 500
    vips = 1000
    net.repulsion(node_distance=100, spring_length=200)

    pool_file = f"{path}/pool.json"
    items = read_file(pool_file)

    virtual_file = f"{path}/virtual.json"
    itemsY = read_file(virtual_file)

    # vips
    for it in itemsY:
        vips = vips + 1
        label1 = it['name']
        if 'pool' in it:
            string = it['pool'].replace('/Common/', '')
            label2 = it['destination'].replace('/Common/', '')
            label3 = f"{label1} \n {label2}"
            net.add_node(vips, label=label3, color='#3155a8')

        #    vip2nodes(vips, pools, nodes, string, items)
            pools, nodes = vip2nodes(vips, pools, nodes, string, items, 'default')
                  
        if 'rules' in it:
            irule_file = f"{path}/irules.json"
            itemI = read_file(irule_file)
            for i in itemI:
                irule_name = i['name']
                search_string = "pool"
                next_string = None
                output = json.dumps(i['apiAnonymous'])
                search_index = output.find(search_string)
                if search_index != -1:
                    # If the search string is found, try to read the next string
                    next_index = search_index + len(search_string)
                    next_string = output[next_index:].split()[0]
                    pool_name = remove_speacial_char(next_string)
                    pools, nodes = vip2nodes(vips, pools, nodes, pool_name, items, irule_name)


if __name__ == "__main__":
    add_obj()
    net.show_buttons(filter_=True)
    net.show(f'{sys.argv[1]}/edges_{sys.argv[1]}.html')
