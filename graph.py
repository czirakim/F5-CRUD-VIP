from pyvis.network import Network
import json

net = Network()
obj_list = []


# add pools,nodes and vips
def add_pool_node():
    nodes = 0
    pools = 500
    vips = 1000

    with open('pool.json', 'r') as file:
        # Read the contents of the file
        data = file.read()
    file.close()

    # Parse the JSON data
    items = json.loads(data)


    with open('virtual.json', 'r') as file:
        # Read the contents of the file
        data = file.read()
    file.close()

    # Parse the JSON data
    itemsY = json.loads(data)

    for it in itemsY:
        vips = vips + 1
        label = it['name']
        net.add_node(vips, label=label, color='#3155a8')
        string = it['pool'].replace('/Common/', '')

        for item in items:
   #         print(item, pools)
            if (string == item['name']):
                pools = pools + 1
                obj_list.append((vips, pools))    
                label = item['name']
                net.add_node(pools, label=label, color='#3da831')
                members = item['members']


            # nodes of the pools
                for member in members:
                    nodes = nodes + 1
                    label2 = member['name']
                    net.add_node(nodes, label=label2, color='#9a31a8')
                    obj_list.append((pools, nodes))

    net.add_edges(obj_list)
  #  print(obj_list)


if __name__ == "__main__":
    add_pool_node()
    net.show('nodes.html')
    net.show('edges.html')
    net.show_buttons(filter_=['physics'])
