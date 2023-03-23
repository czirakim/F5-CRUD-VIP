"""
Create graph

"""

from pyvis.network import Network
import os
import sys
import json
import re

net = Network()

# options for graph
options = {
  "edges": {
    "color": {
      "inherit": True
    },
    "font": {
      "align": "top"
    },
    "selfReferenceSize": 0,
    "selfReference": {
      "angle": 0.7853981633974483
    },
    "smooth": False
  },
  "layout": {
    "hierarchical": {
      "enabled": True,
      "levelSeparation": -240,
      "direction": "DU",
      "sortMethod": "directed",
      "shakeTowards": "roots"
    }
  }
  }


# Get the current working directory and build the path for teh json file
cwd = os.getcwd()
path = f"{cwd}/{sys.argv[1]}"


# read a file
def read_file(name_file):
    with open(f'{name_file}', 'r') as file:
        # Read the contents of the file
        data1 = file.read()
        data = json.loads(data1, strict=False)

    file.close()
    return data


# add nodes and edges to the graph: vip-->pool-->nodes
def vip2nodes(vips, pools, nodes, pool_name, items, label_string):
    # vip --> pool
    for item in items:
        if 'else' in pool_name:
            pool_name = pool_name.replace('else ', '')
            label_string = label_string + ' else '
        if (pool_name == item['name']):
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


# get the uri in if statements
def get_uri_pool_IF(item):
    tmp = re.findall(r"\[HTTP::uri\](.*)", item)
    tmp1 = tmp[0].split('"')
    uri = 'uri:'+tmp1[1]
    pool = re.findall(r"pool (.*?) ", item)
    else_pool = re.findall(r"else(.*) pool (.*?) ", item)
    for i in range(len(pool)):
        for n in range(len(else_pool)):
            if pool[i] in else_pool[n]:
                pool[i] = 'else ' + pool[i]
                # print(pool[i])
    return uri, pool


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
        # draw if vip has default pool
        if 'pool' in it:
            string = it['pool'].replace('/Common/', '')
            label2 = it['destination'].replace('/Common/', '')
            label3 = f"{label1} \n {label2}"
            net.add_node(vips, label=label3, color='#3155a8')
            pools, nodes = vip2nodes(vips, pools, nodes, string, items, 'default')
        # draw if vip has irules
        if 'rules' in it:
            irule_file = f"{path}/irules.json"
            itemI = read_file(irule_file)
            for item in itemI:
                data1 = item["apiAnonymous"]
                irule_name = item["name"]
                uri, pool = get_uri_pool_IF(data1)
                print(pool)
                for name in pool:
                    # with uri
                    # pools, nodes = vip2nodes(vips, pools, nodes, name, items, uri)
                    # with irule name
                    pools, nodes = vip2nodes(vips, pools, nodes, name, items, irule_name)


if __name__ == "__main__":
    add_obj()
    net.show_buttons(filter_=True)
    net.options.__dict__.update(options)
    net.show(f'{sys.argv[1]}/edges_{sys.argv[1]}.html')
