from pyvis.network import Network
import json

net = Network()


# add pools,nodes and vips
def add_obj():
    nodes = 0
    pools = 500
    vips = 1000
    net.repulsion(node_distance=100, spring_length=200)

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

    # vips
    for it in itemsY:
        vips = vips + 1
        label = it['name']
        net.add_node(vips, label=label, color='#3155a8')
        string = it['pool'].replace('/Common/', '')

        # vip --> pool
        for item in items:
            if (string == item['name']):
                pools = pools + 1
                label = item['name']
                net.add_node(pools, label=label, color='#3da831')
                members = item['members']
                net.add_edges([(vips, pools, 5)])

                # pool --> nodes
                for member in members:
                    nodes = nodes + 1
                    label2 = member['name']
                    net.add_node(nodes, label=label2, color='#9a31a8')
                    net.add_edges([(pools, nodes, 2)])


if __name__ == "__main__":
    add_obj()
    net.show('nodes.html')
    net.show('edges.html')
