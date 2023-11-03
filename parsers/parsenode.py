import os
from ..classes.locations.node import Node
import re

def parse_node(node_text, event_dict, encounter_dict, town_dict):
    lines = node_text.strip().split('\n')
    header = lines[0].strip()
    node_number, node_name = header.split('. ', 1)
    node_number = int(node_number.replace('#', '').strip())  # Strip out the '#' and any padding spaces

    # Extract the type and linked name of the game element this node holds
    element_type = lines[2].strip('## ').lower()
    linked_element_name = lines[3].strip('[]')  # Removing the brackets from the linked element name

    # Fetch the game element from the appropriate dictionary
    game_element = None
    if element_type == 'event':
        game_element = event_dict.get(linked_element_name)
    elif element_type == 'encounter':
        game_element = encounter_dict.get(linked_element_name)
    elif element_type == 'town':
        game_element = town_dict.get(linked_element_name)

    if game_element is None:
        raise ValueError(f"{element_type.title()} '{linked_element_name}' is not defined.")

    # Create the node without connections initially
    node = Node(node_number, node_name, game_element)

    # Parse the connection data using a regular expression
    connection_data = []
    connection_pattern = r'- \[\[\((\d+)\)\. ([^\]]+)\]\] : (\d+)'
    for line in lines[5:]:  # Connections are after the fifth line
        match = re.match(connection_pattern, line.strip())
        if match:
            connected_node_number, connected_node_name, distance = match.groups()
            connection_data.append((int(connected_node_number), connected_node_name, float(distance)))

    return node, connection_data



def connect_nodes(nodes_dict, connections_data):
    for node, connection_lines in connections_data.items():
        for connected_node_number, connected_node_name, distance in connection_lines:
            # Here we use the node number and name to find the correct node
            # Assuming that the node name is unique enough or you could enhance this to make sure it matches the number as well
            connected_node = next((n for n in nodes_dict.values() if n.number == connected_node_number and n.name == connected_node_name), None)
            
            if connected_node:
                node.connect_nodes(connected_node, distance)
            else:
                raise ValueError(f"Node '{connected_node_number}. {connected_node_name}' is not defined.")

def parse_all_nodes(nodes_texts, event_dict, encounter_dict, town_dict):
    nodes_dict = {}
    connections_data = {}

    # First pass: create nodes
    for node_text in nodes_texts:
        node, connection_data = parse_node(node_text, event_dict, encounter_dict, town_dict)
        nodes_dict[node.name] = node
        connections_data[node.name] = connection_data

    # Second pass: connect nodes
    connect_nodes(nodes_dict, connections_data)

    return nodes_dict

def read_node_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def parse_directory_nodes(directory_path, event_dict, encounter_dict, town_dict):
    nodes_texts = []
    for filename in os.listdir(directory_path):
        if filename.endswith('.md'):
            file_path = os.path.join(directory_path, filename)
            node_text = read_node_file(file_path)
            nodes_texts.append(node_text)
    return parse_all_nodes(nodes_texts, event_dict, encounter_dict, town_dict)

def generate_nodes_dict(tier: int, event_dict, encounter_dict, town_dict):
    """Generate nodes dictionary for the given tier"""
    nodes_directory = f'vault/t{tier}/nodes'
    return parse_directory_nodes(nodes_directory, event_dict, encounter_dict, town_dict)