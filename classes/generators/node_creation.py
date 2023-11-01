from ..locations.node import Node


class NodeBuilder:
    def __init__(self):
        self.nodes = []

    def create_node(self, number, name, event_or_encounter, travel_description):
        node = Node(number, name, event_or_encounter, travel_description)
        self.nodes.append(node)
        return node

    def link_nodes(self, node1, node2, travel_time):
        node1.connect_nodes(node2, travel_time)

    def display_nodes(self):
        for node in self.nodes:
            print(node)

    def return_nodes(self):
        return self.nodes
